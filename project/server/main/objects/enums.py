
import enum

class FormEnum(enum.Enum):
    @classmethod
    def choices(cls):
        return [(choice, choice.name) for choice in cls]

    @classmethod
    def coerce(cls, item):
        return cls(int(item)) if not isinstance(item, cls) else item

    def __str__(self):
        return str(self.value)
    
class SubmoduleType(FormEnum):
    Default = 1
    List = 2
    Stack = 3
    Presentation = 4


class TemplateInputType(FormEnum):
    Project = 1
    Module = 2
    Submodule = 3

class GeneratedSubmoduleState:
    def __init__(self, name: str, type: str):
        self.name = name
        self.type = type

class GeneratedSubmoduleRepresentation:
    def __init__(self, name: str, type: str, items):
        self.name = name
        self.type = type
        self.items = items