from datetime import datetime
import re
from project.server import db


class Parameter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    action_id = db.Column(db.Integer, db.ForeignKey('action.id'))

    name = db.Column(db.String(140), nullable=False)

    is_array = db.Column(db.Boolean, default=False)
    is_optional = db.Column(db.Boolean, default=False)
    generic_of = db.Column(db.String(140))
    is_optional_generic = db.Column(db.Boolean, default=False)
    default_value = db.Column(db.String(140))
    type = db.Column(db.String(140), nullable=False)

    __table_args__ = (db.UniqueConstraint('action_id', 'name', name='unique_parameter_name_per_action'),)
 
    def next_parameter(self):
        return Parameter.query.filter(Parameter.id>self.id, Parameter.action_id==self.action_id).first()
    
    def previous_parameter(self):
        return Parameter.query.filter(Parameter.id<self.id, Parameter.action_id==self.action_id).first()
    

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
    
        # Used in calling functions
    # name: name: name
    # token: token
    def as_function_call_pair(self):
        name = ""
        if self.name is not None and len(self.name) > 0:
            name = self.name
        return "{name}: {name}".format(name=name)
    
    # used in action enum call
    # {name}: {type}
    # token: TaskResult<String>
    def as_type_repr(self):
        type_text = self.as_only_type()
        if self.generic_of is not None and len(self.generic_of) > 0:
            optinal_generic = self.is_optional_generic is not False and "?" or ""
            return "{name}: {generic_name}<{type}>{is_optional_generic}".format(name=self.name, generic_name=self.generic_of, type=type_text,is_optional_generic=optinal_generic)
        else:
            return "{name}: {type}".format(name=self.name, type=type_text)
        
    # used in action enum call
    # Item, Item?, [Item], [Item]?
    # 
    def as_only_type(self):
        is_optional_string = ""
        if self.is_optional == True:
            is_optional_string += "?"

        if self.is_array == True:
            return "[{type}]{is_optional}".format(type=self.type,is_optional=is_optional_string)
        else:
            return "{type}{is_optional}".format(type=self.type,is_optional=is_optional_string)
    

