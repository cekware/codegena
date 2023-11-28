

from dataclasses import dataclass
from typing import List

from server.main.objects.swift.swift_parameter import SwiftParameter


@dataclass(unsafe_hash=True)
class SwiftTCAAction:
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
    