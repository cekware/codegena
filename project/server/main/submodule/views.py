from flask import render_template, Blueprint, url_for, redirect
from project.server import db

submodule_blueprint = Blueprint("submodule", __name__, template_folder="templates")

from project.server.main.objects.module import Module
from project.server.main.objects.submodule import Submodule
from project.server.main.objects.enums import SubmoduleType
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import ValidationError, DataRequired, Length, Regexp

class SubmoduleForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    reference = SelectField('Reference', choices=[], validators=[DataRequired()])
    default_value = StringField('Default Value')
    is_optional = BooleanField('Optional')
    presentation_type = SelectField('Presentation Type', choices=SubmoduleType.choices, coerce=SubmoduleType.coerce)
    submit = SubmitField('Save')
    
@submodule_blueprint.route('/module/<int:module_id>/submodule', methods=["GET"])
def index(module_id):
    model = Module.query.filter_by(id=module_id).first_or_404()
    project= model.project
    return render_template('submodules.html', data=model.submodules, form=None, selected_submodule=None, project=project, module=model)

@submodule_blueprint.route('/module/<module_id>/add/submodule/type/<int:type>', methods=["GET"])
def add(module_id, type):
    module = Module.query.filter_by(id=module_id).first_or_404()
    presentation_type = SubmoduleType(type)
    submodule = Submodule.new_submodule(module=module,presentation_type=presentation_type)
    db.session.add(submodule)
    db.session.commit()
    return redirect(url_for('submodule.index', module_id=module.id))

@submodule_blueprint.route('/submodule/<int:id>/delete', methods=["GET", "POST", "DELETE"])
def delete(id):
    submodule = Submodule.query.filter_by(id=id).first_or_404()
    module_id= submodule.module.id
    db.session.delete(submodule)
    db.session.commit()
    return redirect(url_for('submodule.index', module_id=module_id))
    
@submodule_blueprint.route('/submodule/<int:id>/edit', methods=["GET", "POST"])
def edit(id):
    model = Submodule.query.filter_by(id=id).first_or_404()
    project= model.module.project
    form = SubmoduleForm()

    choices = map(lambda x: (x.id, x.name), project.modules)
    form.reference.choices = list(choices)

    if form.validate_on_submit():
        model.name = form.name.data
        model.default_value = form.default_value.data
        model.is_optional = form.is_optional.data
        model.presentation_type = form.presentation_type.data
        model.reference_id = form.reference.data
        db.session.commit()
        return redirect(url_for('submodule.index', module_id=model.module.id))
    else:
        form.presentation_type.default = model.presentation_type.value
        form.reference.default = model.reference_id
        form.process()
        form.name.data = model.name
        form.default_value.data = model.default_value
        form.is_optional.data = model.is_optional

    return render_template('submodules.html', data=model.module.submodules, form=form, selected_submodule=model, project=project, module=model.module)