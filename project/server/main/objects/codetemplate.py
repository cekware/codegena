
from datetime import datetime
import os
from project.server import db
import re

class CodeTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

    name = db.Column(db.String(140), nullable=False)
    content = db.Column(db.Text(), nullable=False)

    __table_args__ = (db.UniqueConstraint('project_id', 'name', name='unique_codetemplate_name_per_project'),)

    @classmethod
    def new_template_empty(cls, project):
        content_file='../../../client/static/templates/swift/tca/example1.txt'
        name="NewTemplate"
        modules = CodeTemplate.query.filter(CodeTemplate.project_id == project.id, CodeTemplate.name.like('NewTemplate%')).all()
        if len(modules) > 0:
            max_number = 0
            for module in modules:
                value = re.search(r'\d+', module.name)
                if not value:
                    value = "0"
                else:
                    value = value.group(0)
                number = int(value)
                if max_number < number:
                    max_number = number
            max_number += 1
            name = "{}{}".format(name, max_number)

        basedir = os.path.abspath(os.path.dirname(__file__))
        data_file = os.path.join(basedir, content_file)
        with open(data_file, 'r') as file:
            data = file.read()
     

        return CodeTemplate(name=name, content=data, project=project)
    
    @classmethod
    def new_template(cls, project, name="NewTemplate", content_file='../../../client/static/templates/swift/tca/example1.txt'):
        modules = CodeTemplate.query.filter(CodeTemplate.project_id == project.id, CodeTemplate.name.like('NewTemplate%')).all()
        if len(modules) > 0:
            max_number = 0
            for module in modules:
                value = re.search(r'\d+', module.name)
                if not value:
                    value = "0"
                else:
                    value = value.group(0)
                number = int(value)
                if max_number < number:
                    max_number = number
            max_number += 1
            name = "{}{}".format(name, max_number)

        basedir = os.path.abspath(os.path.dirname(__file__))
        data_file = os.path.join(basedir, content_file)
        with open(data_file, 'r') as file:
            data = file.read()
     

        return CodeTemplate(name=name, content=data, project=project)


