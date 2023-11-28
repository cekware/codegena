from flask import render_template, Blueprint, jsonify, request, current_app, url_for, redirect
from authlib.integrations.flask_client import OAuth
from github import Github, Auth, GithubIntegration
from flask import request
from project.server.main.tasks import create_task
import base64
from flask_login import login_user, logout_user, current_user, login_required

from project.server.main.objects.action import Action
from project.server.main.objects.parameter import Parameter
import json
from project.server import db

parameter_blueprint = Blueprint("parameter", __name__, template_folder="templates")

from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField, IntegerField, FieldList, FormField
from wtforms.validators import ValidationError, DataRequired, Length, Regexp
from wtforms.widgets import HiddenInput

from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

class EntryForm(FlaskForm):
    name_field = StringField('Key')
    value_field = StringField('Value')

class ParameterForm(FlaskForm):
    id = IntegerField(widget=HiddenInput())
    name = StringField('Name', validators=[DataRequired()])
    type = StringField('Type', validators=[DataRequired()])
    extras = FieldList(FormField(EntryForm))
    submit = SubmitField('Save')


@parameter_blueprint.route("/action/<int:action_id>/parameter", methods=["GET"])
def index(action_id):
    model = Action.query.filter_by(id=action_id).first_or_404()
    project = model.module.project
    module = model.module
    return render_template("parameters.html", data=model.parameters, project=project, module=module, action=model, form=None, selected_parameter=None)

@parameter_blueprint.route("/parameter/<int:id>", methods=["GET", "POST"])
def parameter(id):
    parameter = Parameter.query.filter_by(id=id).first_or_404()
    action = parameter.action
    module = action.module
    project = module.project
    form = ParameterForm()
    if form.validate_on_submit():
        parameter.name = form.name.data
        parameter.type = form.type.data
        info = {}
        for entry in form.extras.data:
            info[entry['name_field']] = entry['value_field']
        parameter.extra_info = json.dumps(info)
        db.session.commit()
        return redirect(url_for('parameter.index', action_id=action.id))
    else:
        form.name.data = parameter.name
        form.type.data = parameter.type
        if parameter.extra_info is not None:
            data = json.loads(parameter.extra_info)
            if data is None:
                data = {}
            for k,v in data.items():
                item = EntryForm()
                item.name_field = k
                item.value_field = v
                form.extras.append_entry(item)

    return render_template("parameter.html", form=form, project=project, module=module, action=action, parameter=parameter)

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
        db.session.commit()
        return redirect(url_for('parameter.index', action_id=action.id))
    else:
        form.name.data = model.name
        form.type.data = model.type


    return render_template("parameters.html", data=action.parameters, project=project, module=module, action=action, form=form, selected_parameter=model)

@parameter_blueprint.route("/parameter/<int:id>/addExtra", methods=["GET"])
@login_required
def add_key_value(id):
    parameter = Parameter.query.filter_by(id=id).first_or_404()
    data = None
    if parameter.extra_info is not None:
        data = json.loads(parameter.extra_info)
    
    if data is None:
        data = {}
    count = len(data)
    data["key{}".format(count)] = "value"

    parameter.extra_info = json.dumps(data)
    db.session.commit()
    return redirect(url_for('parameter.parameter', id=parameter.id))

@parameter_blueprint.route("/parameter/<int:id>/deleteExtra/<key>", methods=["GET"])
@login_required
def delete_key_value(id, key):
    parameter = Parameter.query.filter_by(id=id).first_or_404()
    # extras-0-name_field
    data = json.loads(parameter.extra_info)
    del data[key]

    parameter.extra_info = json.dumps(data)
    db.session.commit()
    return redirect(url_for('parameter.parameter', id=parameter.id))