from flask import render_template, Blueprint, jsonify, request, current_app, url_for, redirect
from authlib.integrations.flask_client import OAuth
from github import Github, Auth, GithubIntegration
from flask import request
from project.server.main.tasks import create_task
import base64
from flask_login import login_user, logout_user, current_user, login_required

from project.server.main.objects.module import Module
from project.server.main.objects.action import Action
from project.server.main.objects.parameter import Parameter

from project.server import db

action_blueprint = Blueprint("action", __name__, template_folder="templates")

@action_blueprint.route("/module/<int:module_id>/action", methods=["GET"])
def index(module_id):
    model = Module.query.filter_by(id=module_id).first_or_404()
    project = model.project
    return render_template("actions.html", data=model.actions, project=project, module=model, selected_action=None, form=None)

@action_blueprint.route("/action/<int:id>", methods=["GET"])
@login_required
def action(id):
    model = Action.query.filter_by(id=id).first_or_404()
    project = model.module.project
    titles = [('name', 'Name')]
    return render_template("action.html", data=model.parameters, titles=titles, model=Parameter, project=project, module=model.module, action=model)

@action_blueprint.route("/module/<int:module_id>/action/add", methods=["GET"])
@login_required
def add(module_id):
    module = Module.query.filter_by(id=module_id).first_or_404()
    model = Action.new_action(module=module)
    db.session.add(model)
    db.session.commit()
    return redirect(url_for('action.index', module_id=module_id))

@action_blueprint.route("/action/<id>/delete", methods=["GET", "POST"])
@login_required
def delete(id):
    model = Action.query.filter_by(id=id).first_or_404()
    module_id = model.module.id
    db.session.delete(model)
    db.session.commit()
    return redirect(url_for('action.index', module_id=module_id))

from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import ValidationError, DataRequired, Length, Regexp
class ActionForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Regexp('^\w+$', message="No whitespace")])
    submit = SubmitField('Save')

@action_blueprint.route("/action/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit(id):
    model = Action.query.filter_by(id=id).first_or_404()
    project = model.module.project
    form = ActionForm()
    if form.validate_on_submit():
        model.name = form.name.data
        db.session.add(model)
        db.session.commit()
        return redirect(url_for('action.index', module_id=model.module.id))
    else:
        form.name.data = model.name

    return render_template("actions.html", data=model.module.actions, project=project, module=model.module, selected_action=model, form=form)

