from datetime import datetime
import re
from project.server import db
# from project.server.main.objects.module import Module

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
     
        return State(name=name, module=module, type="String")
    

        # @PresentationState var destination: AppModuleOverlayDestination.State?
    # public var path = StackState<TransactionListDestination.State>()
    # var allTransactions: [Transaction] = []
    def as_swift_state_repr(self) -> str:
        type_text = self.as_only_type()
        attribute = self.attribute is not None and self.attribute or ""
        mutability = self.is_mutable == True and "var" or "let"
        default_value = ""
        if self.default_value is not None and self.default_value != "":
            default_value = " = " + self.default_value

        header = "{}".format(self.access_control)
        if self.attribute is not None and self.attribute != "":
            header = "{} {}".format(self.attribute, self.access_control)

        if self.generic_of is not None and self.generic_of != "":
            is_generic_optional = self.is_optional_generic == True and "?" or ""
            return "{header} {mutability} {name}: {generic_name}<{type}>{optional}{default_value}".format(header=header, mutability=mutability, name=self.name, type=type_text, generic_name=self.generic_of, optional=is_generic_optional, default_value=default_value)    
        else:
            return "{header} {mutability} {name}: {type}{default_value}".format(header=header, mutability=mutability, name=self.name, type=type_text, default_value=default_value)
    
    def as_swift_tca_submodule_state_repr(self) -> str:
        result = "case {}({}.State)".format(self.name, self.type)

        return result

    # used in action enum call
    # {name}: {type}
    # token: TaskResult<String>
    def as_swift_init_parameter_repr(self):
        type_text = self.as_only_type()
        defaultValue = ""
        if self.default_value is not None and self.default_value != "":
            defaultValue = " = " + self.default_value
        elif self.is_optional or self.is_optional_generic:
            defaultValue = " = nil"
        if self.generic_of is not None and len(self.generic_of) > 0:
            optinal_generic = self.is_optional_generic is not None and "?" or ""
            return "{name}: {generic_name}<{type}>{is_optional_generic}{defaultValue}".format(name=self.name, generic_name=self.generic_of, type=type_text,is_optional_generic=optinal_generic, defaultValue=defaultValue)
        else:
            return "{name}: {type}{defaultValue}".format(name=self.name, type=type_text, defaultValue=defaultValue)
        
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
