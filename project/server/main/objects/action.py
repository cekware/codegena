
from datetime import datetime
import re
from project.server import db
from project.server.main.objects.parameter import Parameter, ParameterProxy
from dataclasses import dataclass
import json
# struct/enum
class Action(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))

    name = db.Column(db.String(140), nullable=False)
    parameters = db.relationship('Parameter', backref='action')
    description = db.Column(db.String(1024))
    extra_info = db.Column(db.String(2048))

    __table_args__ = (db.UniqueConstraint('module_id', 'name', name='unique_action_name_per_module'),)

    def get_key(self, key):
        data = {}
        if self.extra_info is not None:
            data = json.loads(self.extra_info)
        return data.get(key, "")


    @classmethod
    def new_action(cls, module):
        name="newAction"
        actions = Action.query.filter(Action.module_id == module.id, Action.name.like('newAction%')).all()
        if len(actions) > 0:
            max_number = 0
            for action in actions:
                value = re.search(r'\d+', action.name)
                if not value:
                    value = "0"
                else:
                    value = value.group(0)
                number = int(value)
                if max_number < number:
                    max_number = number
            max_number += 1
            name = "{}{}".format(name, max_number)
     
        return Action(name=name, description="Action Description", module=module)
    
@dataclass
class ActionProxy:
    name: str
    extra_info: dict
    parameters: list[ParameterProxy]
    description: str

    def __init__(self, name: str, parameters: list[Parameter], extra_info: dict, description: str):
        self.name=name
        self.extra_info=extra_info
        self.description=description
        self.parameters=[
            ParameterProxy(
                name=p.name, 
                type=p.type, 
                extra_info=p.extra_info
            ) 
            for p in parameters
        ]

    def __init__(self, name: str, parameters: list[ParameterProxy], extra_info: dict, description: str):
        self.name=name
        self.extra_info=extra_info
        self.parameters=parameters
        self.description=description

    def extra_dict(self):
        return self.extra_info