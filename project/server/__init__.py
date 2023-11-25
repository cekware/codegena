# project/server/__init__.py


import os

from flask import Flask, request
from flask_bootstrap import Bootstrap4
from authlib.integrations.flask_client import OAuth
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_wtf import CSRFProtect
from flasgger import Swagger
from logging.handlers import RotatingFileHandler

import logging
import traceback
from time import strftime

db = SQLAlchemy()
oauth = OAuth()
login = LoginManager()
login.login_view = 'main.home'
login.login_message = 'Please log in to access this page.'

def create_app(script_info=None):
    # instantiate the app
    app = Flask(
        __name__,
        template_folder="../client/templates",
        static_folder="../client/static",
    )

    # set config
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    
    # set up extensions
    Bootstrap4(app)
    db.init_app(app)
    oauth.init_app(app)
    login.init_app(app)
    csrf = CSRFProtect(app)

    with app.app_context():
        db.create_all()

    app.jinja_env.globals.update(b64_encode=b64_encode)

    swagger = Swagger(app)

    oauth.register(
        name='github',
        client_id=app.config['GH_CLIENT_ID'],
        client_secret=app.config['GH_CLIENT_SECRET'],
        access_token_url='https://github.com/login/oauth/access_token',
        access_token_params=None,
        authorize_url='https://github.com/login/oauth/authorize',
        authorize_params=None,
        api_base_url='https://api.github.com/',
        client_kwargs={'scope': 'user:email'},
    )

    # register blueprints
    from project.server.main.views import main_blueprint
    app.register_blueprint(main_blueprint)

    from project.server.main.project.views import project_blueprint
    app.register_blueprint(project_blueprint)

    from project.server.main.module.views import module_blueprint
    app.register_blueprint(module_blueprint)

    from project.server.main.action.views import action_blueprint
    app.register_blueprint(action_blueprint)

    from project.server.main.state.view import state_blueprint
    app.register_blueprint(state_blueprint)

    from project.server.main.parameter.views import parameter_blueprint
    app.register_blueprint(parameter_blueprint)

    from project.server.main.codetemplates.views import codetemplate_blueprint
    app.register_blueprint(codetemplate_blueprint)

    from project.server.main.submodule.views import submodule_blueprint
    app.register_blueprint(submodule_blueprint)
    
    from project.server.main.moduleimport.views import moduleimport_blueprint
    app.register_blueprint(moduleimport_blueprint)

    # shell context for flask cli
    app.shell_context_processor({"app": app, 'db': db})

    if True:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/automat.log', maxBytes=10240,
                                        backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Automat startup')

    return app




import base64
def b64_encode(str):
    return base64.b64encode(str.encode("utf-8"))