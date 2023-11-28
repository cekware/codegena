

from dataclasses import dataclass

from ..enums import SubmoduleType

# from swiftstate import SwiftState
@dataclass(unsafe_hash=True)
class SwiftSubmodule:
    name: str
    type: str
    presentation_type: SubmoduleType
    extra_info: dict

    @property
    def scope(self) -> str:
        if self.presentation_type == SubmoduleType.Default:
            return "Scope(state: \.{}, action: /Action.{}) {{ {}() }}".format(self.name,self.name, self.type)
        if self.presentation_type == SubmoduleType.List:
            return ".forEach(\.{}, action: /Action.{}(id:action:)){{ {}() }}".format(self.name,self.name, self.type)
        if self.presentation_type == SubmoduleType.Stack:
            return ".forEach(\.path, action: /Action.path) {{ {}Destination() }}".format(self.type)
        if self.presentation_type == SubmoduleType.Presentation:            
            return ".ifLet(\.$sheet, action: /Action.sheet) {{ {}Sheet() }}".format(self.type)
        return "{}".format(self.presentation_type)