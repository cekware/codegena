from datetime import datetime
import re
from project.server import db
from dataclasses import dataclass
import json

class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))

    attribute = db.Column(db.String(140))
    access_control = db.Column(db.String(140), default="public")
    is_mutable = db.Column(db.Boolean, default=True)
    name = db.Column(db.String(140), nullable=False)

    is_array = db.Column(db.Boolean, default=False)
    is_optional = db.Column(db.Boolean, default=False)
    generic_of = db.Column(db.String(140))
    is_optional_generic = db.Column(db.Boolean, default=False)
    default_value = db.Column(db.String(140))
    type = db.Column(db.String(140), nullable=False)

    extra_info = db.Column(db.String(2048))
    description = db.Column(db.String(1024))
    # prop/enum
    identifier = db.Column(db.String(140))

    __table_args__ = (db.UniqueConstraint('module_id', 'name', name='unique_state_name_per_module'),)

    @classmethod
    def new_state(cls, module):
        name="newState"
        states = State.query.filter(State.module_id == module.id, State.name.like('newState%')).all()
        if len(states) > 0:
            max_number = 0
            for state in states:
                value = re.search(r'\d+', state.name)
                if not value:
                    value = "0"
                else:
                    value = value.group(0)
                number = int(value)
                if max_number < number:
                    max_number = number
            max_number += 1
            name = "{}{}".format(name, max_number)
     
        return State(name=name, module=module, access_control="public", description="State Description", is_mutable=True, type="String")
    
@dataclass
class StateProxy:
    access_control: str
    is_mutable: bool
    name: str
    type: str
    extra_info = dict
    description: str

    def __init__(self, access_control: str, is_mutable: bool, name: str, type: str, extra_info: dict, description: str):
        self.access_control = access_control
        self.is_mutable = is_mutable
        self.name = name
        self.type = type
        self.extra_info = extra_info
        self.description = description

    def extra_dict(self):
        return self.extra_info