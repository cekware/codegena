from flask import render_template, Blueprint, url_for, redirect
from project.server import db
import json
from flask_login import login_user, logout_user, current_user, login_required

submodule_blueprint = Blueprint("submodule", __name__, template_folder="templates")

from project.server.main.objects.module import Module
from project.server.main.objects.submodule import Submodule
from project.server.main.objects.enums import SubmoduleType
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField, FieldList, FormField
from wtforms.validators import ValidationError, DataRequired, Length, Regexp

class EntryForm(FlaskForm):
    name_field = StringField('Key')
    value_field = StringField('Value')

class SubmoduleForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    reference = SelectField('Reference', choices=[], validators=[DataRequired()])
    presentation_type = SelectField('Presentation Type', choices=SubmoduleType.choices, coerce=SubmoduleType.coerce)
    extras = FieldList(FormField(EntryForm))
    submit = SubmitField('Save')
    
@submodule_blueprint.route('/module/<int:module_id>/submodule', methods=["GET"])
@login_required
def index(module_id):
    model = Module.query.filter_by(id=module_id).first_or_404()
    project= model.project
    return render_template('submodules.html', data=model.submodules, form=None, selected_submodule=None, project=project, module=model)

@submodule_blueprint.route('/submodule/<int:id>', methods=["GET", "POST"])
@login_required
def submodule(id):
    submodule = Submodule.query.filter_by(id=id).first_or_404()
    module = submodule.module
    project = module.project
    form = SubmoduleForm()

    choices = map(lambda x: (x.id, x.name), project.modules)
    form.reference.choices = list(choices)

    if form.validate_on_submit():
        submodule.name = form.name.data
        submodule.presentation_type = form.presentation_type.data
        submodule.reference_id = form.reference.data
        info = {}
        for entry in form.extras.data:
            info[entry['name_field']] = entry['value_field']
        submodule.extra_info = json.dumps(info)
        db.session.commit()
        db.session.commit()
        return redirect(url_for('submodule.index', module_id=module.id))
    else:
        form.presentation_type.default = submodule.presentation_type.value
        form.reference.default = submodule.reference_id
        form.process()
        if submodule.extra_info is not None:
            data = json.loads(submodule.extra_info)
            if data is None:
                data = {}
            for k,v in data.items():
                item = EntryForm()
                item.name_field = k
                item.value_field = v
                form.extras.append_entry(item)
        form.name.data = submodule.name

    return render_template('submodule.html', project=project, module=module, submodule=submodule, form=form)

@submodule_blueprint.route('/module/<module_id>/add/submodule/type/<int:type>', methods=["GET"])
@login_required
def add(module_id, type):
    module = Module.query.filter_by(id=module_id).first_or_404()
    presentation_type = SubmoduleType(type)
    submodule = Submodule.new_submodule(module=module,presentation_type=presentation_type)
    db.session.add(submodule)
    db.session.commit()
    return redirect(url_for('submodule.index', module_id=module.id))

@submodule_blueprint.route('/submodule/<int:id>/delete', methods=["GET", "POST", "DELETE"])
@login_required
def delete(id):
    submodule = Submodule.query.filter_by(id=id).first_or_404()
    module_id= submodule.module.id
    db.session.delete(submodule)
    db.session.commit()
    return redirect(url_for('submodule.index', module_id=module_id))
    
@submodule_blueprint.route('/submodule/<int:id>/edit', methods=["GET", "POST"])
@login_required
def edit(id):
    model = Submodule.query.filter_by(id=id).first_or_404()
    project= model.module.project
    form = SubmoduleForm()

    choices = map(lambda x: (x.id, x.name), project.modules)
    form.reference.choices = list(choices)

    if form.validate_on_submit():
        model.name = form.name.data
        model.presentation_type = form.presentation_type.data
        model.reference_id = form.reference.data
        db.session.commit()
        return redirect(url_for('submodule.index', module_id=model.module.id))
    else:
        form.presentation_type.default = model.presentation_type.value
        form.reference.default = model.reference_id
        form.process()
        form.name.data = model.name

    return render_template('submodules.html', data=model.module.submodules, form=form, selected_submodule=model, project=project, module=model.module)



@submodule_blueprint.route("/submodule/<int:id>/addExtra", methods=["GET"])
@login_required
def add_key_value(id):
    submodule = Submodule.query.filter_by(id=id).first_or_404()
    data = None
    if submodule.extra_info is not None:
        data = json.loads(submodule.extra_info)
    
    if data is None:
        data = {}
    count = len(data)
    data["key{}".format(count)] = "value"

    submodule.extra_info = json.dumps(data)
    db.session.commit()
    return redirect(url_for('submodule.submodule', id=submodule.id))

@submodule_blueprint.route("/submodule/<int:id>/deleteExtra/<key>", methods=["GET"])
@login_required
def delete_key_value(id, key):
    submodule = Submodule.query.filter_by(id=id).first_or_404()
    # extras-0-name_field
    data = json.loads(submodule.extra_info)
    del data[key]

    submodule.extra_info = json.dumps(data)
    db.session.commit()
    return redirect(url_for('submodule.submodule', id=submodule.id))