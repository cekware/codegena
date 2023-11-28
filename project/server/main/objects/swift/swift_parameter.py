from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class SwiftParameter:
    name: str
    generic_of: str
    simple_type: str
    is_generic_optional: bool
    is_optional: bool
    index: int
    extra_info: dict

    def __init__(
            self,
            name: str, 
            generic_of: str, 
            type: str, 
            is_generic_optional: bool, 
            is_optional: bool, 
            index: int, 
            extra_info: dict
        ):
        if name == "":
            if index == 0:
                self.name = "param" 
            else:
                self.name = "param{}".format(index)
        else:
            self.name = name
        
        self.generic_of = generic_of
        self.simple_type = type
        self.is_generic_optional = is_generic_optional
        self.is_optional = is_optional
        self.index = index
        self.extra_info = extra_info

    def __repr__(self) -> str:
        # transaction(id :ForgotPasswordModule.State.ID, action :ForgotPasswordModule.Action)
        return "{name} {type}".format(
            name=self.name != "" and "{}:".format(self.name) or "",  
            type=self.type,
        )

    @property
    def type(self):
        # Generic<ViewModel?>?
        return "{generic_of}{generic_left_brace}{simple_type}{is_optional}{generic_right_brace}{is_generic_optional}".format(
            generic_of=self.generic_of is not None and self.generic_of or "", 
            simple_type=self.simple_type,
            is_optional=self.is_optional == True and "?" or "",
            is_generic_optional=self.is_generic_optional == True and "?" or "",
            generic_left_brace=self.generic_of is not "" and "<" or "",
            generic_right_brace=self.generic_of is not "" and ">" or ""
        )
