from flask import render_template, Blueprint, url_for, redirect
from flask_login import login_required
from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField, FieldList, FormField
from wtforms.validators import ValidationError, DataRequired, Length, Regexp

from project.server.main.objects.module import Module
from project.server.main.objects.state import State

from project.server import db
import json
state_blueprint = Blueprint("state", __name__, template_folder="templates")

class EntryForm(FlaskForm):
    name_field = StringField('Key')
    value_field = StringField('Value')

class StateForm(FlaskForm):
    name = StringField('Name')
    access_control = StringField('Access Control')
    type = StringField('Type')
    is_mutable = BooleanField('Mutable')

    description = StringField('Description')

    extras = FieldList(FormField(EntryForm))
    
    submit = SubmitField('Save')

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

@state_blueprint.route("/state/<int:id>/addExtra", methods=["GET"])
@login_required
def add_key_value(id):
    state = State.query.filter_by(id=id).first_or_404()
    data = None
    if state.extra_info is not None:
        data = json.loads(state.extra_info)
    
    if data is None:
        data = {}
    count = len(data)
    data["key{}".format(count)] = "value"

    state.extra_info = json.dumps(data)
    db.session.commit()
    return redirect(url_for('state.state', id=state.id))

@state_blueprint.route("/state/<int:id>/deleteExtra/<key>", methods=["GET"])
@login_required
def delete_key_value(id, key):
    state = State.query.filter_by(id=id).first_or_404()
    # extras-0-name_field
    data = json.loads(state.extra_info)
    del data[key]

    state.extra_info = json.dumps(data)
    db.session.commit()
    return redirect(url_for('state.state', id=state.id))


@state_blueprint.route("/state/<int:id>", methods=["GET", "POST"])
def state(id):
    state = State.query.filter_by(id=id).first_or_404()
    module = state.module
    project = module.project
    form = StateForm()
    if form.validate_on_submit():
        state.name = form.name.data
        state.access_control = form.access_control.data
        state.type = form.type.data
        state.is_mutable = form.is_mutable.data
        state.description = form.description.data
        info = {}
        for entry in form.extras.data:
            info[entry['name_field']] = entry['value_field']
        state.extra_info = json.dumps(info)

        db.session.commit()
        # return info
        return redirect(url_for('state.index', module_id=module.id))
    else:
        form.name.data = state.name
        form.access_control.data = state.access_control
        form.type.data = state.type
        form.is_mutable.data = state.is_mutable
        form.description.data = state.description
        if state.extra_info is not None:
            data = json.loads(state.extra_info)
            if data is None:
                data = {}
            for k,v in data.items():
                item = EntryForm()
                item.name_field = k
                item.value_field = v
                form.extras.append_entry(item)

           

    return render_template("state.html",state=state, form=form, module=module, project=project)

@state_blueprint.route("/state/<int:id>/delete", methods=["GET", "POST", "DELETE"])
@login_required
def delete(id):
    model = State.query.filter_by(id=id).first_or_404()
    module_id = model.module.id
    db.session.delete(model)
    db.session.commit()
    return redirect(url_for('state.index', module_id=module_id))



#  access_control: str
#     is_mutable: bool
#     name: str
#     type: str
#     description: str
# class StateForm(FlaskForm):
#     name = StringField('Name')
#     access_control = StringField('Access Control')
#     type = StringField('Type')
#     is_mutable = BooleanField('Mutable')

#     description = StringField('Description')
    
#     submit = SubmitField('Save')

@state_blueprint.route("/state/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit(id):
    model = State.query.filter_by(id=id).first_or_404()
    project = model.module.project
    form = StateForm()
    if form.validate_on_submit():
        model.name = form.name.data
        model.access_control = form.access_control.data
        model.type = form.type.data
        model.is_mutable = form.is_mutable.data
        model.description = form.description.data
        db.session.commit()
        return redirect(url_for('state.index', module_id=model.module.id))
    else:
        form.name.data = model.name
        form.access_control.data = model.access_control
        form.type.data = model.type
        form.is_mutable.data = model.is_mutable
        form.description.data = model.description
    return render_template("states.html", data=model.module.states, selected_state=model, form=form, module=model.module, project=project)


    