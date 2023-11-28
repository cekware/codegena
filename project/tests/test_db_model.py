# project/tests/test_main.py


import unittest

from base import BaseTestCase

from project.server.main.objects.project import Project
from project.server.main.objects.module import Module
from project.server.main.objects.state import State
from project.server.main.objects.action import Action
from project.server.main.objects.parameter import Parameter

from project.server.main.objects.user import User
from project.server.main.objects.project import ProjectProxy


class TestDBModel(BaseTestCase):
    def test_projecy(self):
        # Ensure Flask is setup.

        user = User(login="test", name="test")
 
        project = Project.new_project(user)
        module = Module.new_module(project)
        
        
        state = State.new_state(module)
        module.states.append(
            state
        )
        action = Action.new_action(module)
        module.actions.append(
            action
        )
      
        self.assertEqual(len(user.projects), 1)

        proxy = ProjectProxy(
            name=project.name, 
            description=project.description, 
            modules=project.modules,
            templates=project.templates, 
            extra_info=project.extra_info
        )

        self.assertEqual(proxy.name, project.name)
        self.assertEqual(proxy.description, project.description)
        self.assertEqual(len(proxy.modules), len(project.modules))
        self.assertEqual(len(proxy.templates), len(project.templates))
        self.assertEqual(proxy.extra_info, project.extra_info)

        self.assertEqual(proxy.modules[0].states[0].name, "newState")
        self.assertEqual(proxy.modules[0].states[0].type, "String")
        self.assertEqual(proxy.modules[0].states[0].access_control, "public")
        self.assertEqual(proxy.modules[0].states[0].is_mutable, True)
        self.assertEqual(proxy.modules[0].states[0].description, "State Description")

        self.assertEqual(proxy.modules[0].actions[0].name, "newAction")
        self.assertEqual(len(proxy.modules[0].actions[0].parameters), 0)
        self.assertEqual(proxy.modules[0].actions[0].description, "Action Description")
        
        


if __name__ == "__main__":
    unittest.main()