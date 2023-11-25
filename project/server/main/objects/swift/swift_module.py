from dataclasses import dataclass
from typing import List
# from enums import SubmoduleType
# from objects.enums import SubmoduleType
# from .enums import SubmoduleType

from .swift_state import SwiftState
from .swift_action import SwiftAction
from .swift_module_import import SwiftModuleImport
from .swift_parameter import SwiftParameter
from .swift_submodule import SwiftSubmodule
from ..enums import SubmoduleType



@dataclass(unsafe_hash=True)
class SwiftModule:
    name: str
    description: str
    states: List[SwiftState]
    actions: List[SwiftAction]
    module_imports: List[SwiftModuleImport]
    submodules: List[SwiftSubmodule]

    def __init__(self, module):
        self.name = module.name
        _imports = []
        _states = []
        _actions = []
        _submodules = []
        for module_import in module.module_imports:
            _imports.append(SwiftModuleImport(name=module_import.name))
        

        for state in module.states:
            _states.append(SwiftState(
                name=state.name,
                attribute=state.attribute,
                simple_type=state.type,
                private_default_value=state.default_value,
                access_control=state.access_control,
                generic_of=state.generic_of,
                is_mutable=state.is_mutable,
                is_optional=state.is_optional,
                is_generic_optional=state.is_optional_generic
                )
            )
        for action in module.actions:
            _parameters = []
            index = 0
            for parameter in action.parameters:
                _parameters.append(
                    SwiftParameter(
                        index=index,
                        simple_name=parameter.name,
                        generic_of=parameter.generic_of,
                        simple_type=parameter.type,
                        is_generic_optional=parameter.is_optional_generic,
                        is_optional=parameter.is_optional
                        )
                    )
                index += 1
            _actions.append(
                SwiftAction(
                    name=action.name,
                    module_name=action.module.name,
                    parameters=_parameters
                )
            )

        for submodule in module.submodules:
            name=submodule.name
            attribute=None
            type=None
            default_value=None
            access_control="public"
            generic_of=None
            is_mutable=True
            is_optional=False
            is_optional_generic=False
            ref_name = ""
            if submodule.reference is not None:
                ref_name = (submodule.reference.name is not None and submodule.reference.name or "")
            else:
                ref_name = "#Error"
            _submodules.append(
                SwiftSubmodule(
                    name=name,
                    type=ref_name,
                    presentation_type=submodule.presentation_type
                )
            )
            
            if submodule.presentation_type == SubmoduleType.Default:
                type = "{}.State".format(ref_name)
                default_value = ".init()"
                _actions.append(
                    SwiftAction(
                        name=name,
                        module_name=submodule.type,
                        parameters=[
                            SwiftParameter(
                                index=0,
                                simple_name="",
                                generic_of=None,
                                simple_type="{}.Action".format(ref_name),
                                is_generic_optional=False,
                                is_optional=False
                            )
                        ]
                    )
                )
            if submodule.presentation_type == SubmoduleType.List:
                type = "IdentifiedArrayOf<{}.State>".format(ref_name)
                default_value = "[]"
                # case transactions(id: TransactionModule.State.ID, moduleAction: TransactionModule.Action)
                _actions.append(
                    SwiftAction(
                        name=name,
                        module_name=submodule.type,
                        parameters=[
                            SwiftParameter(
                                index=0,
                                simple_name="id",
                                generic_of=None,
                                simple_type="{}.State.ID".format(ref_name),
                                is_generic_optional=False,
                                is_optional=False
                            ),
                            SwiftParameter(
                                index=1,
                                simple_name="action",
                                generic_of=None,
                                simple_type="{}.Action".format(ref_name),
                                is_generic_optional=False,
                                is_optional=False
                            )
                        ]
                    )
                )
            if submodule.presentation_type == SubmoduleType.Stack:
                type = "{}Destination.State".format(submodule.type)
                default_value = ".init()"
                generic_of = "StackState"
                _actions.append(
                    SwiftAction(
                        name="path",
                        module_name=submodule.type,
                        parameters=[
                            SwiftParameter(
                                index=0,
                                simple_name="",
                                generic_of="StackAction",
                                simple_type="{type}Destination.State, {type}Destination.Action".format(type=submodule.type),
                                is_generic_optional=False,
                                is_optional=False
                            )
                        ]
                    )
                )
                
            if submodule.presentation_type == SubmoduleType.Presentation:
                type = "{}Sheet.State".format(submodule.type)
                default_value = "nil"
                is_optional_generic = True
                attribute = "@PresentationState"
                _actions.append(
                    SwiftAction(
                        name="sheet",
                        module_name=submodule.type,
                        parameters=[
                            SwiftParameter(
                                index=0,
                                simple_name="",
                                generic_of=None,
                                simple_type="{}Sheet.Action".format(submodule.type),
                                is_generic_optional=False,
                                is_optional=False
                            )
                        ]
                    )
                )
    
            _states.append(
                SwiftState(
                    name=name,
                    attribute=attribute,
                    simple_type=type,
                    private_default_value=default_value,
                    access_control=access_control,
                    generic_of=generic_of,
                    is_mutable=is_mutable,
                    is_optional=is_optional,
                    is_generic_optional=is_optional_generic
                )
            )
            
           

        self.states = _states
        self.actions = _actions
        self.submodules = sorted(_submodules, key=lambda x: x.presentation_type.value, reverse=True) 
        self.module_imports = _imports

    @property
    def imports(self):
        names = ["import {}".format(x.name) for x in self.module_imports]
        return "\n".join(names)
    
    @property
    def initializer(self):
        values = ["{name}: {type}{default_value}".format(name=x.name, type=x.type, default_value=x.equal_default_value) for x in self.states]
        inner = ",\n\t\t\t".join(values)
        body_values = ["{name} = {name}".format(name=x.name, type=x.type, default_value=x.default_value) for x in self.states]
        body = "\n\t\t\t\t".join(body_values)
        return "public init(\n\t\t\t{inner}\n\t\t) {{\n\t\t\t\t{body}\n\t\t}}".format(inner=inner, body=body)