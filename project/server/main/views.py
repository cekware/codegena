# project/server/main/views.py


import redis
from rq import Queue, Connection
from flask import render_template, Blueprint, jsonify, request, current_app, url_for, redirect
from authlib.integrations.flask_client import OAuth
from github import Github, Auth, GithubIntegration
from flask import request, send_from_directory
from project.server.main.tasks import create_export_task
from flask_login import login_user, logout_user, current_user
from project.server import oauth
from project.server.main.objects.project import Project
from project.server.main.objects.user import User
from project.server import db



main_blueprint = Blueprint("main", __name__,)
@main_blueprint.route("/", methods=["GET"])
def home():
    if current_user.is_authenticated:
        return redirect(url_for('project.index'))
    else:
        return render_template("main/guess.html",current_user=current_user)

@main_blueprint.route('/login')
def registro():
   github = oauth.create_client('github')
#    redirect_uri = url_for('main.authorize', _external=True)
   return github.authorize_redirect()

@main_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))



@main_blueprint.route('/authorize')
def authorize():
   g = Github()
   client_id= current_app.config["GH_CLIENT_ID"]
   client_secret=current_app.config["GH_CLIENT_SECRET"]
   app = g.get_oauth_application(client_id, client_secret)
   code = request.args.get('code')
   token = app.get_access_token(code)
   auth = app.get_app_user_auth(token)
   g = Github(auth=auth)
   id = g.get_user().id
   login = g.get_user().login
   name = g.get_user().name
  
   user = User.query.filter_by(id=id).first()
   if user is None:
        user = User(id=id, login=login, name=name)

   user.code = token.token
   db.session.add(user)
   db.session.commit()
    
   login_user(user, remember=True)
   return redirect(url_for('main.home'))

@main_blueprint.route('/docs/<path:path>')
def send_docs(path):
    # basedir = os.path.abspath(os.path.dirname(__file__))
    # basedir = os.path.join(basedir, '../../../docs/_build/html/index.html')
    # f = open(basedir, "r")
    # return f.read()
    return send_from_directory('static', path)

@main_blueprint.route("/export/async/<int:id>", methods=["GET"])
def export_async(id):
    with Connection(redis.from_url(current_app.config["REDIS_URL"])):
        q = Queue()
        task = q.enqueue(create_export_task, id)
    response_object = {
        "status": "success",
        "data": {
            "task_id": task.get_id()
        }
    }
    return jsonify(response_object), 202


@main_blueprint.route("/tasks/<task_id>", methods=["GET"])
def get_status(task_id):
    with Connection(redis.from_url(current_app.config["REDIS_URL"])):
        q = Queue()
        task = q.fetch_job(task_id)
    if task:
        response_object = {
            "status": "success",
            "data": {
                "task_id": task.get_id(),
                "task_status": task.get_status(),
                "task_result": task.result,
            },
        }
    else:
        response_object = {"status": "error"}
    return jsonify(response_object)



@main_blueprint.route('/colors/<palette>/')
def colors(palette):
    """Example endpoint returning a list of colors by palette
    This is using docstrings for specifications.
    ---
    parameters:
      - name: palette
        in: path
        type: string
        enum: ['all', 'rgb', 'cmyk']
        required: true
        default: all
    definitions:
      Palette:
        type: object
        properties:
          palette_name:
            type: array
            items:
              $ref: '#/definitions/Color'
      Color:
        type: string
    responses:
      200:
        description: A list of colors (may be filtered by palette)
        schema:
          $ref: '#/definitions/Palette'
        examples:
          rgb: ['red', 'green', 'blue']
    """
    all_colors = {
        'cmyk': ['cyan', 'magenta', 'yellow', 'black'],
        'rgb': ['red', 'green', 'blue']
    }
    if palette == 'all':
        result = all_colors
    else:
        result = {palette: all_colors.get(palette)}

    return jsonify(result)