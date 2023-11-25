from flask import render_template, Blueprint, jsonify, request, current_app, url_for, redirect
from authlib.integrations.flask_client import OAuth
from github import Github, Auth, GithubIntegration
from flask import request
from project.server.main.tasks import create_task
import base64
from flask_login import login_user, logout_user, current_user, login_required


from project.server.main.objects.project import Project
from project.server.main.objects.codetemplate import CodeTemplate

from project.server import db

codetemplate_blueprint = Blueprint("codetemplate", __name__, template_folder="templates")

from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import ValidationError, DataRequired, Length, Regexp
class CodeTemplateForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    content = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Save')

@codetemplate_blueprint.route("/project/<int:project_id>/template", methods=["GET"])
def index(project_id):
    model = Project.query.filter_by(id=project_id).first_or_404()
    return render_template("templates.html", data=model.templates, selected_template=None, form=None, project=model)

@codetemplate_blueprint.route("/template/<int:id>", methods=["GET", "POST"])
@login_required
def template(id):
    model = CodeTemplate.query.filter_by(id=id).first_or_404()
    form = CodeTemplateForm()
    if form.validate_on_submit():
        model.name = form.name.data
        model.content = form.content.data
        db.session.commit()
        return redirect(url_for('codetemplate.index', project_id=model.project.id))
    else:
        # form.type.default = model.type.value
        form.process()
        form.name.data = model.name
        form.content.data = model.content
    return render_template("template.html", data=model, form=form, project=model.project, template=model)

@codetemplate_blueprint.route("/project/<int:project_id>/template/add", methods=["GET"])
@login_required
def add(project_id):
    project = Project.query.filter_by(id=project_id).first_or_404()
    model = CodeTemplate.new_template_empty(project)
    project.templates.append(model)
    db.session.add(model)
    db.session.commit()
    return redirect(url_for('codetemplate.index', project_id=project_id))

@codetemplate_blueprint.route("/template/<id>/delete", methods=["GET", "POST", "DELETE"])
@login_required
def delete(id):
    model = CodeTemplate.query.filter_by(id=id).first_or_404()
    project_id = model.project.id
    db.session.delete(model)
    db.session.commit()
    return redirect(url_for('codetemplate.index', project_id=project_id))


@codetemplate_blueprint.route("/template/<int:id>/update", methods=["GET", "POST"])
@login_required
def edit(id):
    model = CodeTemplate.query.filter_by(id=id).first_or_404()
    form = CodeTemplateForm()
    if form.validate_on_submit():
        model.name = form.name.data
        db.session.commit()
        return redirect(url_for('codetemplate.index', project_id=model.project.id))
    else:
        form.name.data = model.name
        return render_template("templates.html", data=model.project.templates, selected_template=model, form=form, project=model.project)