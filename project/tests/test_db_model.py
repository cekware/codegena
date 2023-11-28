# project/tests/test_main.py


import unittest

from base import BaseTestCase

from project.server.main.objects.project import Project
from project.server.main.objects.module import Module
from project.server.main.objects.state import State
from project.server.main.objects.action import Action
from project.server.main.objects.parameter import Parameter
from project.server.main.objects.codetemplate import CodeTemplate
from project.server.main.objects.moduleimport import ModuleImport
from project.server.main.objects.submodule import Submodule
from project.server.main.objects.enums import SubmoduleType
from project.server.main.objects.user import User
from project.server.main.objects.project import ProjectProxy


class TestDBModel(BaseTestCase):
    def test_projecy(self):
        # Ensure Flask is setup.

        user = User(login="test", name="test")
 
        project = Project.new_project(user)
        module = Module.new_module(project)
        ModuleImport.new_module_import(module)

        Submodule.new_submodule(module=module, presentation_type=SubmoduleType.Default, reference=module)
        Submodule.new_submodule(module=module, presentation_type=SubmoduleType.List, reference=module)
        Submodule.new_submodule(module=module, presentation_type=SubmoduleType.Presentation, reference=module)
        Submodule.new_submodule(module=module, presentation_type=SubmoduleType.Stack, reference=module)
        
        state = State.new_state(module)
        module.states.append(
            state
        )
        action = Action.new_action(module)
        module.actions.append(
            action
        )

        template = CodeTemplate.new_template(project)

        parameter = Parameter.new_parameter(action)
      
        self.assertEqual(len(user.projects), 1)

        proxy = ProjectProxy(
            name=project.name, 
            description=project.description, 
            modules=project.modules,
            templates=project.templates, 
            extra_info=project.extra_info
        )
        # Project
        self.assertEqual(proxy.name, project.name) # name: str
        self.assertEqual(proxy.description, project.description) # description: str
        self.assertEqual(len(proxy.modules), len(project.modules)) # modules: list[ModuleProxy]
        self.assertEqual(len(proxy.templates), len(project.templates)) # templates = list[CodeTemplateProxy]
        self.assertEqual(proxy.extra_info, project.extra_info) # extra_info = dict
        # Module
        self.assertEqual(proxy.modules[0].name, "NewModule") # name: str
        self.assertEqual(proxy.modules[0].description, "Module description") # description: str
        self.assertEqual(proxy.modules[0].extra_info, {}) #extra_info = dict
        # ModuleImport
        self.assertEqual(proxy.modules[0].module_imports[0].name, "NewLibrary") # name: str
        # Submodule
        self.assertEqual(proxy.modules[0].submodules[0].name, "newSubmodule") # name: str
        self.assertEqual(proxy.modules[0].submodules[0].type, "NewModule") # type: str
        self.assertEqual(proxy.modules[0].submodules[0].extra_info, {}) # extra_info: dict
        self.assertEqual(proxy.modules[0].submodules[0].presentation_type, SubmoduleType.Default) # presentation_type: SubmoduleType

        self.assertEqual(proxy.modules[0].submodules[1].name, "newSubmodule") # name: str
        self.assertEqual(proxy.modules[0].submodules[1].type, "NewModule") # type: str
        self.assertEqual(proxy.modules[0].submodules[1].extra_info, {}) # extra_info: dict
        self.assertEqual(proxy.modules[0].submodules[1].presentation_type, SubmoduleType.List) # presentation_type: SubmoduleType

        self.assertEqual(proxy.modules[0].submodules[2].name, "newSubmodule") # name: str
        self.assertEqual(proxy.modules[0].submodules[2].type, "NewModule") # type: str
        self.assertEqual(proxy.modules[0].submodules[2].extra_info, {}) # extra_info: dict
        self.assertEqual(proxy.modules[0].submodules[2].presentation_type, SubmoduleType.Presentation) # presentation_type: SubmoduleType

        self.assertEqual(proxy.modules[0].submodules[3].name, "newSubmodule") # name: str
        self.assertEqual(proxy.modules[0].submodules[3].type, "NewModule") # type: str
        self.assertEqual(proxy.modules[0].submodules[3].extra_info, {}) # extra_info: dict
        self.assertEqual(proxy.modules[0].submodules[3].presentation_type, SubmoduleType.Stack) # presentation_type: SubmoduleType
  
        # States
        self.assertEqual(proxy.modules[0].states[0].name, "newState") # name: str
        self.assertEqual(proxy.modules[0].states[0].type, "String") # type: str
        self.assertEqual(proxy.modules[0].states[0].access_control, "public") # access_control: str
        self.assertEqual(proxy.modules[0].states[0].is_mutable, True) # is_mutable: bool
        self.assertEqual(proxy.modules[0].states[0].description, "State Description") # description: str
        self.assertEqual(proxy.modules[0].states[0].extra_info, dict()) # extra_info: dict
        # Action
        self.assertEqual(proxy.modules[0].actions[0].name, "newAction")
        self.assertEqual(len(proxy.modules[0].actions[0].parameters), 1)
        self.assertEqual(proxy.modules[0].actions[0].description, "Action Description")
        # Parameter
        self.assertEqual(proxy.modules[0].actions[0].parameters[0].name, "param")
        self.assertEqual(proxy.modules[0].actions[0].parameters[0].type, "String")

        # CodeTemplate
        self.assertEqual(len(proxy.templates), 1)
        


if __name__ == "__main__":
    unittest.main()