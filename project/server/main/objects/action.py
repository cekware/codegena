
from datetime import datetime
import re
from project.server import db

# struct/enum
class Action(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))

    name = db.Column(db.String(140), nullable=False)
    parameters = db.relationship('Parameter', backref='action')

    extra_info = db.Column(db.String(2048))

    __table_args__ = (db.UniqueConstraint('module_id', 'name', name='unique_action_name_per_module'),)


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
     
        return Action(name=name, module=module)
    
    def swift_enum_repr(self) -> str:
        parameters = self.swift_parameters_repr()
        if parameters is not None:
            return "case {name}({parameters})".format(name=self.name, parameters=parameters)
        else:
            return "case {name}".format(name=self.name)
        
    def swift_parameters_repr(self):
        if self.parameters is not None and len(self.parameters) == 0:
            return None
        params = []
        for parameter in self.parameters:
            params.append(parameter.as_type_repr())

        return "{result}".format(result=", ".join(params))
    
    def swift_tca_func_definition_repr(self):
        parameters = self.swift_parameters_repr()
        module_name = self.module.name
        tca_addon = "state: inout {module_name}.State".format(module_name=module_name)
        if parameters is None:
            return "private func {name}({tca_addon}) -> Effect<{module_name}.Action>".format(name=self.name, tca_addon=tca_addon, module_name=module_name)
        else:
            return "private func {name}({parameters}, {tca_addon}) -> Effect<{module_name}.Action>".format(name=self.name, parameters=parameters,module_name=module_name,tca_addon=tca_addon)
        

    def as_swift_tca_submodule_action_repr(self):
        result = "case {}({}.Action)".format(self.name, self.module_name)
        return result
