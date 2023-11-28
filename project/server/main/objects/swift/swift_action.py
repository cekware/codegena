

from dataclasses import dataclass
from typing import List

from .swift_parameter import SwiftParameter


@dataclass(unsafe_hash=True)
class SwiftAction:
    name: str
    module_name: str
    parameters: List[SwiftParameter]
    extra_info: dict
    
    def __repr__(self) -> str:
        # case updateNetworkConnection(status: NWPath.Status)
        return "{name}{left_parenthesis}{parameters}{right_parenthesis}".format(
            name=self.name, 
            parameters=self.parameters_string,
            left_parenthesis=self.parameters_string != "" and "(" or "",
            right_parenthesis=self.parameters_string != "" and ")" or ""
            )
    
    @property
    def parameters_string(self) -> str:
        names = ["{}".format(x) for x in self.parameters]
        if len(names) == 0:
            return ""
        result = ", ".join(names)
        return "{}".format(result)
    
    @property
    def parameters_let_case(self) -> str:
        names = ["let {}".format(x.name) for x in self.parameters]
        if len(names) == 0:
            return ""
        result = ", ".join(names)
        return "({})".format(result)
    
    @property
    def parameters_func_case(self) -> str:
        names = ["{}: {}".format(x.name, x.type) for x in self.parameters]
        if len(names) == 0:
            return ""
        result = ", ".join(names)
        return "({})".format(result)
    
    @property
    def parameters_func_call(self) -> str:
        names = ["{name}: {name}".format(name=x.name) for x in self.parameters]
        if len(names) == 0:
            return "{}()".format(self.name)
        result = ", ".join(names)
        return "{name}({parameters})".format(name=self.name,parameters=result)
    
    @property
    def function_definition(self):
        tca_addon = "state: inout {module_name}.State".format(module_name=self.module_name)
        return "private func {name}({parameters}) -> Effect<{module_name}.Action>".format(
            name=self.name,
            parameters=self.parameters_string,
            module_name=self.module_name,
            tca_addon=tca_addon
            )

      
