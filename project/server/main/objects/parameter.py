from datetime import datetime
import re
from project.server import db
from dataclasses import dataclass
import json

class Parameter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    action_id = db.Column(db.Integer, db.ForeignKey('action.id'))

    name = db.Column(db.String(140), nullable=False)
    description = db.Column(db.String(1024))
    is_array = db.Column(db.Boolean, default=False)
    is_optional = db.Column(db.Boolean, default=False)
    generic_of = db.Column(db.String(140))
    is_optional_generic = db.Column(db.Boolean, default=False)
    default_value = db.Column(db.String(140))
    type = db.Column(db.String(140), nullable=False)
    extra_info = db.Column(db.String(2048))
    __table_args__ = (db.UniqueConstraint('action_id', 'name', name='unique_parameter_name_per_action'),)
 
    def next_parameter(self):
        return Parameter.query.filter(Parameter.id>self.id, Parameter.action_id==self.action_id).first()
    
    def previous_parameter(self):
        return Parameter.query.filter(Parameter.id<self.id, Parameter.action_id==self.action_id).first()
    
    def extra_dict(self):
        return self.extra_info is not None and json.loads(self.extra_info) or dict()

    @classmethod
    def new_parameter(cls, action):
        name="param"
        parameters = Parameter.query.filter(Parameter.action_id == action.id, Parameter.name.like('param%')).all()
        if len(parameters) > 0:
            max_number = 0
            for parameter in parameters:
                value = re.search(r'\d+', parameter.name)
                if not value:
                    value = "0"
                else:
                    value = value.group(0)
                number = int(value)
                if max_number < number:
                    max_number = number
            max_number += 1
            name = "{}{}".format(name, max_number)
     
        return Parameter(name=name, action=action, type="String")

@dataclass
class ParameterProxy:
    name: str
    type: str
    extra_info: dict
 
    def __init__(self, name, type, extra_info):
        self.name = name
        self.type = type
        self.extra_info = extra_info

    def extra_dict(self):
        return self.extra_info