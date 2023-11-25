from flask import render_template, Blueprint, url_for, redirect
from flask_login import login_required

from project.server.main.objects.module import Module
from project.server.main.objects.state import State

from project.server import db

state_blueprint = Blueprint("state", __name__, template_folder="templates")

@state_blueprint.route("/module/<int:module_id>/state", methods=["GET"])
def index(module_id):
    model = Module.query.filter_by(id=module_id).first_or_404()
    project = model.project
    return render_template("states.html", data=model.states, selected_state=None, form=None, module=model, project=project)

@state_blueprint.route("/module/<int:module_id>/state/add", methods=["GET"])
@login_required
def add(module_id):
    module = Module.query.filter_by(id=module_id).first_or_404()
    model = State.new_state(module=module)
    db.session.add(model)
    db.session.commit()
    return redirect(url_for('state.index', module_id=module_id))

@state_blueprint.route("/state/<int:id>/delete", methods=["GET", "POST", "DELETE"])
@login_required
def delete(id):
    model = State.query.filter_by(id=id).first_or_404()
    module_id = model.module.id
    db.session.delete(model)
    db.session.commit()
    return redirect(url_for('state.index', module_id=module_id))

from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import ValidationError, DataRequired, Length, Regexp


class StateForm(FlaskForm):
    name = StringField('Name')
    attribute = StringField('Attribute')
    access_control = StringField('Access Control')
    type = StringField('Type')
    is_mutable = BooleanField('Mutable')
    is_array = BooleanField('Array')
    is_optional = BooleanField('Optional')

    generic_of = StringField('Generic Of')
    is_optional_generic = BooleanField('Optional Generic')
    default_value = StringField('Default Value')
    
    submit = SubmitField('Save')

@state_blueprint.route("/state/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit(id):
    model = State.query.filter_by(id=id).first_or_404()
    project = model.module.project
    form = StateForm()
    if form.validate_on_submit():
        model.name = form.name.data
        model.attribute = form.attribute.data
        model.access_control = form.access_control.data
        model.type = form.type.data
        model.is_mutable = form.is_mutable.data
        model.is_array = form.is_array.data
        model.is_optional = form.is_optional.data
        model.generic_of = form.generic_of.data
        model.is_optional_generic = form.is_optional_generic.data
        model.default_value = form.default_value.data
        db.session.commit()
        return redirect(url_for('state.index', module_id=model.module.id))
    else:
        form.name.data = model.name
        form.attribute.data = model.attribute
        form.access_control.data = model.access_control
        form.type.data = model.type
        form.is_mutable.data = model.is_mutable
        form.is_array.data = model.is_array
        form.is_optional.data = model.is_optional
        form.generic_of.data = model.generic_of
        form.is_optional_generic.data = model.is_optional_generic
        form.default_value.data = model.default_value
    return render_template("states.html", data=model.module.states, selected_state=model, form=form, module=model.module, project=project)


    