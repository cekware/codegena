from flask import render_template, Blueprint, jsonify, request, current_app, url_for, redirect
from authlib.integrations.flask_client import OAuth
from github import Github, Auth, GithubIntegration
from flask import request
from project.server.main.tasks import create_task
import base64
from flask_login import login_user, logout_user, current_user, login_required

from project.server.main.objects.action import Action
from project.server.main.objects.parameter import Parameter

from project.server import db

parameter_blueprint = Blueprint("parameter", __name__, template_folder="templates")

from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Length, Regexp
from wtforms.widgets import HiddenInput

from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class ParameterForm(FlaskForm):
    id = IntegerField(widget=HiddenInput())
    name = StringField('Name', validators=[DataRequired()])
    is_array = BooleanField('Array')
    is_optional = BooleanField('Optional')
    generic_of = StringField('Generic Of')
    is_optional_generic = BooleanField('Optional')
    default_value = StringField('Default Value')
    type = StringField('Type', validators=[DataRequired()])
    submit = SubmitField('Save')


@parameter_blueprint.route("/action/<int:action_id>/parameter", methods=["GET"])
def index(action_id):
    model = Action.query.filter_by(id=action_id).first_or_404()
    project = model.module.project
    module = model.module
    return render_template("parameters.html", data=model.parameters, project=project, module=module, action=model, form=None, selected_parameter=None)

@parameter_blueprint.route("/action/<int:action_id>/parameter/add", methods=["GET"])
@login_required
def add(action_id):
    module = Action.query.filter_by(id=action_id).first_or_404()
    model = Parameter.new_parameter(action=module)
    db.session.add(model)
    db.session.commit()
    return redirect(url_for('parameter.index', action_id=action_id))

@parameter_blueprint.route("/parameter/<int:id>/delete", methods=["GET", "POST", "DELETE"])
@login_required
def delete(id):
    model = Parameter.query.filter_by(id=id).first_or_404()
    action_id = model.action.id
    db.session.delete(model)
    db.session.commit()
    return redirect(url_for('parameter.index', action_id=action_id))


@parameter_blueprint.route("/parameter/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit(id):
    model = Parameter.query.filter_by(id=id).first_or_404()
    project = model.action.module.project
    module = model.action.module
    action = model.action
    form = ParameterForm()
    if form.validate_on_submit():
        model.name = form.name.data
        model.type = form.type.data
        model.is_array = form.is_array.data
        model.is_optional = form.is_optional.data
        model.generic_of = form.generic_of.data
        model.is_optional_generic = form.is_optional_generic.data
        model.default_value = form.default_value.data
        db.session.commit()
        return redirect(url_for('parameter.index', action_id=action.id))
    else:
        form.name.data = model.name
        form.type.data = model.type
        form.is_array.data = model.is_array
        form.is_optional.data = model.is_optional
        form.generic_of.data = model.generic_of
        form.is_optional_generic.data = model.is_optional_generic
        form.default_value.data = model.default_value

    return render_template("parameters.html", data=action.parameters, project=project, module=module, action=action, form=form, selected_parameter=model)
