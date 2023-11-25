from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class SwiftParameter:
    simple_name: str
    generic_of: str
    simple_type: str
    is_generic_optional: bool
    is_optional: bool
    index: int

    def __repr__(self) -> str:
        # transaction(id :ForgotPasswordModule.State.ID, action :ForgotPasswordModule.Action)
        return "{name}{type}".format(
            name=self.simple_name != "" and "{} :".format(self.simple_name) or "",  
            type=self.type,
        )
    @property
    def name(self) -> str:
        if self.simple_name == "":
            if self.index == 0:
                return "param" 
            return "param{}".format(self.index)
        return self.simple_name
    @property
    def type(self):
        # Generic<ViewModel?>?
        return "{generic_of}{generic_left_brace}{simple_type}{is_optional}{generic_right_brace}{is_generic_optional}".format(
            generic_of=self.generic_of is not None and self.generic_of or "", 
            simple_type=self.simple_type,
            is_optional=self.is_optional == True and "?" or "",
            is_generic_optional=self.is_generic_optional == True and "?" or "",
            generic_left_brace=self.generic_of is not None and "<" or "",
            generic_right_brace=self.generic_of is not None and ">" or ""
        )
