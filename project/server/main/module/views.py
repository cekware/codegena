from flask import render_template, Blueprint, jsonify, request, current_app, url_for, redirect
from authlib.integrations.flask_client import OAuth
from github import Github, Auth, GithubIntegration
from flask import request, Response
from project.server.main.tasks import create_task
import base64
from flask_login import login_user, logout_user, current_user, login_required


from project.server.main.objects.project import Project
from project.server.main.objects.module import Module
from project.server.main.objects.state import State
from project.server.main.objects.action import Action
from project.server.main.objects.parameter import Parameter
from project.server.main.objects.submodule import Submodule
from project.server.main.objects.enums import SubmoduleType



from project.server import db

from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Length, Regexp
from wtforms.widgets import HiddenInput

module_blueprint = Blueprint("module", __name__, template_folder="templates")

@module_blueprint.route("/project/<int:project_id>/module", methods=["GET"])
def index(project_id):
    model = Project.query.filter_by(id=project_id).first_or_404()
    return render_template("modules.html", data=model.modules, selected_module=None, project=model, form=None)

class TemplateSelectForm(FlaskForm):
    id = IntegerField(widget=HiddenInput())
    templates = SelectField('Template', validators=[DataRequired()])
    submit = SubmitField('Change')

@module_blueprint.route("/module/<int:id>", methods=["GET", "POST"])
@login_required
def module(id):
    model = Module.query.filter_by(id=id).first_or_404()
    project = model.project
    form = TemplateSelectForm()
    templates = map(lambda x: (x.id, x.name), project.templates)
    form.templates.choices = list(templates)
    if form.validate_on_submit():
        model.selected_template_id = form.templates.data
        db.session.commit()
        return redirect(url_for('module.module', id=id))
    else:
        form.templates.default = model.selected_template_id
        form.process()

    return render_template("module.html", data=model, project=model.project, module=model, form=form)

@module_blueprint.route("/project/<int:project_id>/module/add", methods=["GET"])
@login_required
def add(project_id):
    project = Project.query.filter_by(id=project_id).first_or_404()
    model = Module.new_module(project=project)
    db.session.add(model)
    db.session.commit()
    return redirect(url_for('module.index', project_id=project_id))

class OASImportForm(FlaskForm):
    id = IntegerField(widget=HiddenInput())
    content = StringField('Content', validators=[DataRequired()])
    submit = SubmitField('Import')

from openapi_parser import parse
@module_blueprint.route("/project/<int:project_id>/module/add/oas", methods=["GET", "POST"])
@login_required
def import_oas(project_id):
    project = Project.query.filter_by(id=project_id).first_or_404()
    basedir = os.path.abspath(os.path.dirname(__file__))
    data_file = os.path.join(basedir, '../../../client/static/templates/oas/example1.txt')
    with open(data_file, 'r') as file:
        data = file.read()

    
    specification = parse(spec_string = data)

    # first find all the get operations with array response
    # this means a parent module with a list submodule 

    result = []
    created_objets = []
    for path in specification.paths:
        # Create a module object for every path
        module_name = path.url
        new_module = Module(name=module_name, description=path.description, project=project)
        created_objets.append(new_module)
        for operation in path.operations:
            # Create an action for every operation
            action_name = operation.operation_id
            new_action = Action(name=action_name, module=new_module)
            created_objets.append(new_action)
            for parameter in operation.parameters:
                parameter_name = parameter.name
                parameter_type = parameter.schema.type.value
                if parameter_type == "array":
                    type_override = parameter.schema.items.type.value
                    new_parameter = Parameter(name=parameter_name, action=new_action, type=type_override, is_array=True, is_optional=parameter.required)
                    created_objets.append(new_parameter)
                else:
                    new_parameter = Parameter(name=parameter_name, action=new_action, type=parameter_type)
                    created_objets.append(new_parameter)



            for response in operation.responses:
                if response.code == 200:
                    for type in response.content:
                        if type.type.value == "application/json":
                            if type.schema.type.value == "array":
                                
                                submodule_name = "list"
                                submodule_type = "{}Submodule".format(module_name)

                                # create a module for submodule first 
                                module_for_submodule = submodule_type
                                module_for_submodule = Module(
                                    name=module_for_submodule, 
                                    description="Autogenerated module for {}".format(submodule_name), 
                                    project=project
                                    )
                                created_objets.append(module_for_submodule)
                                # add states

                                # Create a List submodule
                                # other case is probably changing the local state and does not need a submodule

                                submodule = Submodule(
                                    module=new_module, 
                                    name=submodule_name, 
                                    type=submodule_type, 
                                    presentation_type=SubmoduleType.List, 
                                    is_optional=False, 
                                    default_value="[]"
                                )
                                created_objets.append(submodule)
                            else:
                                # not array so add the states to the module
                                new_state = State()

    db.session.add_all(created_objets)
    db.session.commit()
    # return render_template("test.html", specification=specification, result=created_objets)
    return redirect(url_for('module.index', project_id=project_id))
    form = OASImportForm()
    form.content.data = data
    if form.validate_on_submit():
        content = form.content.data

        specification = parse(spec_string = data)
        return render_template("oas_import.html", specification=specification)
        
        # urls = [x.url for x in specification.paths]
        # return urls
        # return redirect(url_for('module.index', project_id=project_id))
    else:
        # return redirect(url_for('module.index', project_id=project_id))
        return render_template("oas_import.html", project=project, form=form)
    # for server in specification.servers:
        # print(f"{server.description} - {server.url}")
    
    # urls = [x.url for x in specification.paths]
    # print(urls)
    # for path in specification.paths:
    #     supported_methods = ','.join([x.method.value for x in path.operations])

    #     print(f"Operation: {path.url}, methods: {supported_methods}")
    
    
    
    
    # project = Project.query.filter_by(id=project_id).first_or_404()
    # model = Module.new_module(project=project)
    # db.session.add(model)
    # db.session.commit()
    return redirect(url_for('module.index', project_id=project_id))



@module_blueprint.route("/module/<int:id>/delete", methods=["GET", "POST", "DELETE"])
@login_required
def delete(id):
    model = Module.query.filter_by(id=id).first_or_404()
    project_id = model.project.id
    db.session.delete(model)
    db.session.commit()
    return redirect(url_for('module.index', project_id=project_id))


class ModuleForm(FlaskForm):
    id = IntegerField(widget=HiddenInput())
    name = StringField('Name', validators=[DataRequired()])
    # is_array = BooleanField('Array')
    # isOptional = BooleanField('Optional')
    # generic_of = StringField('Generic Of')
    # default_value = StringField('Default Value')
    # type = StringField('Type', validators=[DataRequired()])
    submit = SubmitField('Save')

    # def validate_name(self, fieldname):
    #     names_in_db = dict(Parameter.query.with_entities(Parameter.id, Parameter.name).all())
    #     if fieldname.data in names_in_db.values() and fieldname.data != self.old_name:
    #         raise ValidationError('Name must be unique')

@module_blueprint.route("/module/<int:id>/edit", methods=["GET","POST"])
@login_required
def edit(id):
    model = Module.query.filter_by(id=id).first_or_404()
    form = ModuleForm()
    if form.validate_on_submit():
        model.name = form.name.data
        db.session.commit()
        return redirect(url_for('module.index', project_id=model.project.id))
    else:
        form.name.data = model.name
        return render_template("modules.html", data=model.project.modules, selected_module=model, project=model.project, form=form)

import os
from jinja2 import Template, FileSystemLoader, Environment
@module_blueprint.route("/module/<int:id>/export", methods=["GET"])
@login_required
def export(id):
    return ""
    # model = Module.query.filter_by(id=id).first_or_404()

    # export_model = ExportModule.fromModule(model)

    # # basedir = os.path.abspath(os.path.dirname(__file__))
    # static_folder_path = os.path.join(current_app.root_path, current_app.static_folder)
    # data_file = os.path.join(static_folder_path, 'templates/tca')
    
    # env = Environment(
    #     # loader = DictLoader({'index.html': 'source here'})
    #     loader = FileSystemLoader(data_file)
    # )
    
    # template = env.get_template('module.txt')

    # result = template.render(module=export_model)
    # return Response(result, mimetype='text/plain')
