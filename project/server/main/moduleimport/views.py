from flask import render_template, Blueprint, jsonify, request, current_app, url_for, redirect
from authlib.integrations.flask_client import OAuth
from github import Github, Auth, GithubIntegration
from flask import request
from project.server.main.tasks import create_task
import base64
from flask_login import login_user, logout_user, current_user, login_required


from project.server.main.objects.module import Module
from project.server.main.objects.moduleimport import ModuleImport

from project.server import db

moduleimport_blueprint = Blueprint("moduleimport", __name__, template_folder="templates")

from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import ValidationError, DataRequired, Length, Regexp
class ModuleImportForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Regexp('^\w+$', message="No whitespace")])
    function = StringField('Function')
    submit = SubmitField('Save')

@moduleimport_blueprint.route('/module/<int:module_id>/moduleimport', methods=["GET"])
def index(module_id):
    module = Module.query.filter_by(id=module_id).first_or_404()
    project = module.project

    return render_template('moduleimports.html', data=module.module_imports, selected_module_import=None, form=None, project=project, module=module)

@moduleimport_blueprint.route('/moduleimport/<int:id>', methods=["GET", "POST"])
def moduleimport(id):
    model = ModuleImport.query.filter_by(id=id).first_or_404()
    module = model.module
    project = module.project
    form = ModuleImportForm()
    if form.validate_on_submit():
        model.name = form.name.data
        model.function = form.function.data
        db.session.commit()
        return redirect(url_for('moduleimport.index', module_id=module.id))
    else:
        form.name.data = model.name
        form.function.data = model.function
        return render_template('moduleimport.html', data=model, project=project, form=form, module=module, module_import=model)

@moduleimport_blueprint.route('/module/<int:module_id>/add/moduleimport', methods=["GET"])
def add(module_id):
    module = Module.query.filter_by(id=module_id).first_or_404()
    moduleimport = ModuleImport.new_module_import(module=module)
    db.session.add(moduleimport)
    db.session.commit()
    return redirect(url_for('moduleimport.index', module_id=module.id))
        
@moduleimport_blueprint.route('/moduleimport/<int:id>/delete', methods=["GET", "POST", "DELETE"])
def delete(id):
    model = ModuleImport.query.filter_by(id=id).first_or_404()
    module_id= model.module.id
    db.session.delete(model)
    db.session.commit()
    return redirect(url_for('moduleimport.index', module_id=module_id))
    

@moduleimport_blueprint.route('/moduleimport/<int:id>/edit', methods=["GET", "POST"])
def edit(id):
    module_import = ModuleImport.query.filter_by(id=id).first_or_404()
    project = module_import.module.project
    form = ModuleImportForm()
    if form.validate_on_submit():
        module_import.name = form.name.data
        module_import.function = form.function.data
        db.session.commit()
        return redirect(url_for('moduleimport.index', module_id=module_import.module.id))
    else:
        form.name.data = module_import.name
        form.function.data = module_import.function
    return render_template('moduleimports.html', data=module_import.module.module_imports, selected_module_import=module_import, form=form, project=project, module=module_import.module)
