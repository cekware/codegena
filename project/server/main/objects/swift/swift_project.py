
from dataclasses import dataclass
from project.server.main.objects.module import Module
from project.server.main.objects.state import State
from project.server.main.objects.action import Action
from project.server.main.objects.submodule import Submodule
from project.server.main.objects.moduleimport import ModuleImport
from project.server.main.objects.parameter import Parameter
from project.server.main.objects.codetemplate import CodeTemplate



@dataclass(frozen=True)
class SwiftProject:
    name: str
    description: str
    modules: list[Module]
    templates = list[State]
    extra_info = dict