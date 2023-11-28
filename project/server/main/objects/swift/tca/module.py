from dataclasses import dataclass
from typing import List

from project.server.main.objects.swift.swift_submodule import SwiftSubmodule
from project.server.main.objects.swift.swift_module_import import SwiftModuleImport
from project.server.main.objects.swift.swift_state import SwiftState
from project.server.main.objects.swift.swift_action import SwiftAction

 

# from .swift_state import SwiftState
# from .swift_action import SwiftAction
# from .swift_module_import import SwiftModuleImport
# from .swift_parameter import SwiftParameter
# from .swift_submodule import SwiftSubmodule
# from ..enums import SubmoduleType



@dataclass(unsafe_hash=True)
class SwiftTCAModule:
    name: str
    description: str
    states: List[SwiftState]
    actions: List[SwiftAction]
    module_imports: List[SwiftModuleImport]
    submodules: List[SwiftSubmodule]
    extra_info: dict

    def __init__(
            self, 
            name: str, 
            description: str, 
            states: List[SwiftState],
            actions: List[SwiftAction],
            module_imports: List[SwiftModuleImport],
            submodules: List[SwiftSubmodule],
            extra_info: dict
        ):
        self.name = name
        self.description = description
        self.states = states
        self.actions = actions
        self.module_imports = module_imports
        self.submodules = submodules
        self.extra_info = extra_info


    @property
    def body(self):
        
        cases = [
            "case .{name}{parameters_let_case}:\n\t\t\t\treturn self.{parameters_func_call}".format(
            name=x.name,
            parameters_let_case=x.parameters_let_case,parameters_func_call=x.parameters_func_call
            )
            for x in self.actions
        ]
        
        cases = "\n\t\t\t".join(cases)
        scopes = [x.scope for x in self.submodules]
        # scopes = []
        scopes = "\n".join(scopes)
        return "public var body: some ReducerOf<Self> {{\n\tReduce {{ state, action in\n\t\tswitch action {{\n\t\t\t{cases}\n\t\t}}\n\t}}\n\t{scopes} \n}}".format(cases=cases,scopes=scopes)
