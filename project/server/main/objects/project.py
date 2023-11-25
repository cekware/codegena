
from datetime import datetime
import os
from project.server import db
from flask_login import current_user
import re
from flask import current_app

from project.server.main.objects.codetemplate import CodeTemplate

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    name = db.Column(db.String(140), nullable=False)
    description = db.Column(db.String(1024))

    modules = db.relationship('Module', backref='project')
    templates = db.relationship('CodeTemplate', backref='project')

    extra_info = db.Column(db.String(2048))

    __table_args__ = (db.UniqueConstraint('user_id', 'name', name='unique_name_per_user'),)


    @classmethod
    def new_project(cls):
        name="NewProject"
        projects = Project.query.filter(Project.user_id == current_user.id, Project.name.like('NewProject%')).all()
        if len(projects) > 0:
            max_number = 0
            for project in projects:
                value = re.search(r'\d+', project.name)
                if not value:
                    value = "0"
                else:
                    value = value.group(0)
                number = int(value)
                if max_number < number:
                    max_number = number
            max_number += 1
            name = "{}{}".format(name, max_number)
        
        data_file = os.path.join(current_app.root_path, '../client/static/templates/readme/example1.txt')
        with open(data_file, 'r') as file:
            data = file.read()
        return Project(owner=current_user, name=name, description=data)