from dataclasses import dataclass

@dataclass(unsafe_hash=True)
class SwiftState:
    name: str
    attribute: str
    simple_type: str
    private_default_value: str
    access_control: str
    generic_of: str
    is_mutable: bool
    is_optional: bool
    is_generic_optional: bool
    extra_info: dict
    description: str

    def __init__(
        self, 
        name: str,
        attribute: str, 
        simple_type: str,
        private_default_value: str, 
        access_control: str, 
        generic_of: str, 
        is_mutable: bool, 
        is_optional: bool,
        is_generic_optional: bool,
        extra_info: dict,
        description: str
    ):
        self.name = name
        self.attribute = attribute
        self.simple_type = simple_type
        self.private_default_value = private_default_value
        self.access_control = access_control
        self.generic_of = generic_of
        self.is_mutable = is_mutable
        self.is_optional = is_optional
        self.is_generic_optional = is_generic_optional
        self.extra_info = extra_info
        self.description = description


    @property
    def default_value(self):
        if self.private_default_value is not None and self.private_default_value != "":
            return "{}".format(self.private_default_value)
        else:
            return ""
        


    @property
    def type(self):
        # Generic<ViewModel?>?
        generic_name = self.generic_of is not None and self.generic_of or ""
        return "{generic_of}{generic_left_brace}{simple_type}{is_optional}{generic_right_brace}{is_generic_optional}".format(
            generic_of=generic_name, 
            simple_type=self.simple_type,
            is_optional=self.is_optional == True and "?" or "",
            is_generic_optional=self.is_generic_optional == True and "?" or "",
            generic_left_brace=generic_name is not "" and "<" or "",
            generic_right_brace=generic_name is not "" and ">" or ""
        )

    def __repr__(self) -> str:
        # @ObservableObject public var viewModel: Generic<ViewModel?>? = nil

        return "{attribute}{access_control}{is_mutable}{name}: {type}{default_value}".format(
            attribute=self.attribute is not None and self.attribute != "" and "{} ".format(self.attribute) or "",
            access_control=self.access_control is not None and "{} ".format(self.access_control) or "",
            is_mutable=self.is_mutable == True and "var " or "let ", 
            name=self.name, 
            type=self.type,
            default_value=self.default_value is not "" and " = {}".format(self.default_value) or ""
        )