from datetime import datetime
import re
from project.server import db
from project.server.main.objects.enums import SubmoduleType


class Submodule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))
    is_optional = db.Column(db.Boolean, default=False)
    # name, type, parent_module_name

    # Default
    # public var {name}: {type}.State? = nil
    # List
    # public var {name}: IdentifiedArrayOf<{name}.State>
    # Stack
    # public var path: StackState<{parent_module_name}Destination.State> = .init()
    # Presentation
    # @PresentationState public var sheet: {parent_module_name}Sheet.State?

    name = db.Column(db.String(140), nullable=False)
    type = db.Column(db.String(140))
    presentation_type = db.Column(db.Enum(SubmoduleType), nullable=False, default=SubmoduleType.Default)
    default_value = db.Column(db.String(140))

    # 1-to-1 relationship called 'reference' to Module
    reference_id = db.Column(db.Integer, db.ForeignKey('module.id'))
    reference = db.relationship('Module', backref=db.backref('submodule_reference', uselist=False), foreign_keys=[reference_id])

    extra_info = db.Column(db.String(2048))
    __table_args__ = (db.UniqueConstraint('module_id', 'name', name='unique_submodule_name_per_module'),)

    @classmethod
    def new_submodule(cls, module, presentation_type):
        name="newSubmodule"
        submodules = Submodule.query.filter(Submodule.module_id == module.id, Submodule.name.like('newSubmodule%')).all()
        if len(submodules) > 0:
            max_number = 0
            for submodule in submodules:
                value = re.search(r'\d+', submodule.name)
                if not value:
                    value = "0" 
                else:
                    value = value.group(0)
                number = int(value)
                if max_number < number:
                    max_number = number
            max_number += 1
            name = "{}{}".format(name, max_number)


        type = ""
        is_optional = False
        default_value = ""
        if presentation_type == SubmoduleType.Default:
            type = "{}".format(module.name)
        if presentation_type == SubmoduleType.List:
            type = "{}".format(module.name)
            default_value = "[]"
        if presentation_type == SubmoduleType.Stack:
            type = "{}".format(module.name)
            default_value = ".init()"
        if presentation_type == SubmoduleType.Presentation:
            type = "{}".format(module.name)
            default_value = "nil"
            is_optional = True
        # basedir = os.path.abspath(os.path.dirname(__file__))
        # data_file = os.path.join(basedir, '../../client/static/templates/readme/example1.txt')
        # with open(data_file, 'r') as file:
        #     data = file.read()
     
        return Submodule(module=module, name=name, type=type, presentation_type=presentation_type, is_optional=is_optional, default_value=default_value)
    

    def swift_tca_func_definition_repr(self):
        if self.presentation_type == SubmoduleType.Default:
            return "private func {}(action: {}.Action, state: inout {}.State) -> Effect<{}.Action>".format(self.name, self.type,self.module.name, self.module.name)
        if self.presentation_type == SubmoduleType.List:
            return "private func {}(id: {}.State.ID, action: {}.Action, state: inout {}.State) -> Effect<{}.Action>".format(self.name, self.type, self.type,self.module.name,self.type)
        if self.presentation_type == SubmoduleType.Stack:
            return "private func path(path: StackAction<{}Destination.State, {}Destination.Action>, state: inout {}.State) -> Effect<{}.Action>".format(self.module.name, self.module.name,self.module.name, self.module.name)
        if self.presentation_type == SubmoduleType.Presentation:            
            return "private func sheet(action: PresentationAction<{}Sheet.Action>, state: inout {}.State) -> Effect<{}.Action>".format(self.module.name, self.module.name,self.module.name)

    def swift_tca_body_case_repr(self):
        if self.presentation_type == SubmoduleType.Default:
            return "case .{}(let action):\n\t\t\t\t\treturn self.{}(action: action, state: &state)".format(self.name,self.name)
        if self.presentation_type == SubmoduleType.List:
            return "case .{}(let action):\n\t\t\t\t\treturn self.{}(action: action, state: &state)".format(self.name,self.name)
        if self.presentation_type == SubmoduleType.Stack:
            return "case .path(let path):\n\t\t\t\t\treturn self.path(path: path, state: &state)".format(self.name,self.name)
        if self.presentation_type == SubmoduleType.Presentation:            
            return "case .sheet(let action):\n\t\t\t\t\treturn self.sheet(action: action, state: &state)".format(self.name,self.name)

    # return self.{{ action.name }}({% for parameter in action.parameters %}{% if parameter.as_function_call_pair() %}{{ parameter.as_function_call_pair() }}, {% endif %}{% endfor %}

    # @PresentationState var destination: AppModuleOverlayDestination.State?
    # public var path = StackState<TransactionListDestination.State>()
    def as_swift_submodule_default_repr(self) -> str:
        if self.presentation_type == SubmoduleType.Default:
            is_optional = ""
            default_value = ""
            if self.is_optional:
                is_optional = "?"
            if self.default_value is not None and self.default_value != "":
                default_value = " = {}".format(self.default_value)

            return "public var {name}: {type}.State {is_optional}{default_value}".format(name=self.name, type=self.type, is_optional=is_optional, default_value=default_value)
        return ""
        
    def as_swift_submodule_list_repr(self) -> str:
        if self.presentation_type == SubmoduleType.List:
            return "public var {}: IdentifiedArrayOf<{}.State> = []".format(self.name, self.type)
        return ""
        
    def as_swift_submodule_stack_repr(self) -> str:
        if self.presentation_type == SubmoduleType.Stack:
            return "public var path: StackState<{}Destination.State> = .init()".format(self.module.name)
        return ""
        
    def as_swift_submodule_presentation_repr(self) -> str:
        if self.presentation_type == SubmoduleType.Presentation:            
            return "@PresentationState public var sheet: {}Sheet.State? = nil".format(self.module.name)
        return ""
        
    # @PresentationState var destination: AppModuleOverlayDestination.State?
    # public var path = StackState<TransactionListDestination.State>()
    def as_swift_tca_scopes_repr(self) -> str:
        if self.presentation_type == SubmoduleType.Default:
            return "Scope(state: \.{}, action: /Action.{}){{ {}() }}".format(self.name,self.name, self.type)
        if self.presentation_type == SubmoduleType.List:
            return ".forEach(\.{}, action: /Action.{}){{ {}() }}".format(self.name,self.name, self.type)
        if self.presentation_type == SubmoduleType.Stack:
            return ".forEach(\.path, action: /Action.path){{ {}Destination() }}".format(self.module.name)
        if self.presentation_type == SubmoduleType.Presentation:            
            return ".ifLet(\.$sheet, action: /Action.sheet){{ {}Sheet() }}".format(self.module.name)
  
    def as_swift_tca_submodule_action_repr(self) -> str:
        if self.presentation_type == SubmoduleType.Default:
            return "case {}({}.Action)".format(self.name,self.type)
        if self.presentation_type == SubmoduleType.List:
            return "case {}(id: {}.State.ID, action: {}.Action)".format(self.name,self.name,self.type)
        if self.presentation_type == SubmoduleType.Stack:
            return "case {}(StackAction<{}Destination.State, {}Destination.Action>)".format("path", self.module.name,self.module.name)
        if self.presentation_type == SubmoduleType.Presentation:            
            return "case {}(PresentationAction<{}Sheet.Action>)".format("sheet",self.module.name)
        
    # used in action enum call
    # {name}: {type}
    # token: TaskResult<String>
    def as_swift_init_parameter_repr(self):

        if self.presentation_type == SubmoduleType.Default:
            is_optional = ""
            default_value = ""
            if self.is_optional:
                is_optional = "?"
            if self.default_value is not None and self.default_value != "":
                default_value = " = {}".format(self.default_value)
            return "{name}: {type}.State{is_optional}{default_value}".format(name=self.name, type=self.type, is_optional=is_optional, default_value=default_value)
        if self.presentation_type == SubmoduleType.List:
            return "{}: IdentifiedArrayOf<{}.State> = []".format(self.name, self.type)
        if self.presentation_type == SubmoduleType.Stack:
            return "path: StackState<{}Destination.State> = .init()".format(self.module.name)
        if self.presentation_type == SubmoduleType.Presentation:            
            return "sheet: {}Sheet.State? = nil".format(self.module.name)
