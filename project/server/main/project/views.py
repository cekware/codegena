from flask import render_template, Blueprint, jsonify, request, current_app, url_for, redirect
from authlib.integrations.flask_client import OAuth
from github import Github, Auth, GithubIntegration
from flask import request, Response
from project.server.main.tasks import create_task
import base64, os
from flask_login import login_user, logout_user, current_user, login_required

from project.server.main.objects.project import Project
from project.server.main.objects.codetemplate import CodeTemplate


from project.server import db
from jinja2 import Template, FileSystemLoader, Environment

project_blueprint = Blueprint("project", __name__, template_folder='templates')



@project_blueprint.route("/project", methods=["GET"])
@login_required
def index():
    return render_template("projects.html", data=current_user.projects, selected_project=None, form=None)

@project_blueprint.route("/project/<int:id>", methods=["GET"])
@login_required
def project(id):
    model = Project.query.filter_by(id=id).first_or_404()
    return render_template("project.html", data=model, project=model)

@project_blueprint.route("/project/add", methods=["GET"])
@login_required
def add():
    model = Project.new_project(current_user)
    templates = [
        CodeTemplate.new_template(model, name="swift-tca", content_file='../../../client/static/templates/swift/tca/example1.txt'),
        CodeTemplate.new_template(model, name="swift-mvvm", content_file='../../../client/static/templates/swift/mvvm/example1.txt')
    ]
    db.session.add(model)
    db.session.add_all(templates)
    db.session.commit()
    return redirect(url_for('project.index'))

from project.server.main.project.example_project import example_app

@project_blueprint.route("/project/addExample", methods=["GET"])
@login_required
def addExample():
    model = Project.new_project(current_user)
    example_app(
        project=model,
    )
    templates = [
        CodeTemplate.new_template(model, name="swift-tca", content_file='../../../client/static/templates/swift/tca/example1.txt'),
        CodeTemplate.new_template(model, name="swift-mvvm", content_file='../../../client/static/templates/swift/mvvm/example1.txt')
    ]
    db.session.add(model)
    db.session.add_all(templates)
    db.session.commit()
    return redirect(url_for('project.index'))


@project_blueprint.route("/project/<int:id>/delete", methods=["GET", "POST", "DELETE"])
@login_required
def delete(id):
    model = Project.query.filter_by(id=id).first_or_404()
    db.session.delete(model)
    db.session.commit()
    return redirect(url_for('project.index'))

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Length, Regexp
from wtforms.widgets import HiddenInput
class ProjectForm(FlaskForm):
    id = IntegerField(widget=HiddenInput())
    name = StringField('Name', validators=[DataRequired(), Regexp('^[\w-]+$', message="No whitespace")])
    submit = SubmitField('Save')

@project_blueprint.route("/project/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit(id):
    model = Project.query.filter_by(id=id).first_or_404()
    form = ProjectForm()
    if form.validate_on_submit():
        model.name = form.name.data
        db.session.commit()
        return redirect(url_for('project.index'))
    else:
        form.name.data = model.name
        return render_template("projects.html", data=current_user.projects, selected_project=model, form=form)

@project_blueprint.route("/project/<int:id>/update", methods=["GET", "POST"])
@login_required
def update(id):
    model = Project.query.filter_by(id=id).first_or_404()
    return render_template("update.html", data=model)


@project_blueprint.route("/projects/<project_id>/export", methods=["GET"])
@login_required
def project_export(project_id):
    return redirect(url_for('project.index'))
    # project = Project.query.filter_by(id=project_id).first_or_404()

    # basedir = os.path.abspath(os.path.dirname(__file__))
    # data_file = os.path.join(basedir, '../../client/static/templates/tca')
    
    # env = Environment(
    #     loader = FileSystemLoader(data_file)
    # )


    # data = open(pem, 'r').read()
    # auth = Auth.AppAuth(app_id, data)
    # gi = GithubIntegration(auth=auth)
    # g = gi.get_github_for_installation(project.installation_id)
    # repo = g.get_repo(project.name)

    # package_swift_name = "Package.swift"
    # package_template = env.get_template('package.txt')
    # package_swift_content = package_template.render(project=project)
    # try:
    #     contents = repo.get_contents(package_swift_name)
    #     repo.update_file(contents.path, "Update package.swift", package_swift_content, contents.sha)
    # except:
    #     repo.create_file(package_swift_name, "Create package.swift", package_swift_content)
    
    # test_swift_name = "Tests/{}Tests.swift".format(project.short_name)
    # test_template = env.get_template('test.txt')
    # test_swift_content = test_template.render(project=project)
    # try:
    #     contents = repo.get_contents(test_swift_name)
    #     repo.update_file(contents.path, "Update Tests", test_swift_content, contents.sha)
    # except:
    #     repo.create_file(test_swift_name, "Create Tests", test_swift_content)

    # extra_swift_name = "Sources/{}/Extra.swift".format(project.short_name)
    # extra_template = env.get_template('extra_file.txt')
    # extra_swift_content = extra_template.render()
    # try:
    #     contents = repo.get_contents(extra_swift_name)
    #     repo.update_file(contents.path, "Update Extra", extra_swift_content, contents.sha)
    # except:
    #     repo.create_file(extra_swift_name, "Create Extra", extra_swift_content)

    
    # for module in project.modules:
    #     module_name = "Sources/{}/{}.swift".format(project.short_name, module.name)
    #     if module.extra_info == "navigation":
    #         template = env.get_template('navigation.txt')
    #     else:
    #         template = env.get_template('module.txt')

    #     result = template.render(module=module,imports=project.imports)
    #     try:
    #         contents = repo.get_contents(module_name)
    #         repo.update_file(contents.path, "Update {}".format(module.name), result, contents.sha)
    #     except:
    #         repo.create_file(module_name, "Create {}".format(module.name), result)
                     
        
    
    # results = []
    # for module in project.modules:
    #     if module.extra_info == "navigation":
    #         template = env.get_template('navigation.txt')
    #     else:
    #         template = env.get_template('module.txt')
    #     result = template.render(module=module,imports=project.imports)
    #     results.append(result)

    # string = "".join(results)
    # resp = Response(string)
    # resp.headers['Content-Type'] = 'text/plain'
    # return resp