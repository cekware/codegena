
from datetime import datetime
import re
from project.server import db
from dataclasses import dataclass

from project.server.main.objects.enums import SubmoduleType, GeneratedSubmoduleRepresentation, GeneratedSubmoduleState
from jinja2 import Environment, Template, FileSystemLoader, BaseLoader

from project.server.main.objects.codetemplate import CodeTemplate
import json


class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))


    name = db.Column(db.String(140), nullable=False)
    description = db.Column(db.String(1024))
    isPublic = db.Column(db.Boolean, default=True)

    states = db.relationship('State', backref='module')
    actions = db.relationship('Action', backref='module')
    submodules = db.relationship('Submodule', backref='module', foreign_keys='Submodule.module_id')

    module_imports = db.relationship('ModuleImport', backref='module')
    extra_info = db.Column(db.String(2048))

    selected_template_id = db.Column(db.Integer, db.ForeignKey(CodeTemplate.id))

    __table_args__ = (db.UniqueConstraint('project_id', 'name', name='unique_module_name_per_project'),)


    @classmethod
    def new_module(cls, project):
        name="NewModule"
        modules = Module.query.filter(Module.project_id == project.id, Module.name.like('NewModule%')).all()
        if len(modules) > 0:
            max_number = 0
            for module in modules:
                value = re.search(r'\d+', module.name)

                if not value:
                    value = "0"
                else:
                    value = value.group(0)
                number = int(value)
                if max_number < number:
                    max_number = number
            max_number += 1
            name = "{}{}".format(name, max_number)
     
        return Module(name=name, description="Module description", project=project)
    
    def extra_dict(self):
        return self.extra_info is not None and json.loads(self.extra_info) or dict()
    
    def proxy(self):
        return ModuleProxy(
            name=self.name, 
            description=self.description, 
            extra_info=self.extra_dict(), 
            states=self.states, 
            actions=self.actions, 
            submodules=self.submodules, 
            module_imports=self.module_imports
        )

    def as_swift_repr(self):
        if self.selected_template_id is not None:
            code_template = CodeTemplate.query.filter_by(id=self.selected_template_id).first()
        else:
            code_template = CodeTemplate.query.first()

        if code_template is not None:
            template = Environment(loader=BaseLoader()).from_string(code_template.content)
            
            result = template.render(module=self.proxy())
            return result
        else:
            return "{}".format(self.selected_template_id)
    

from project.server.main.objects.state import StateProxy
from project.server.main.objects.action import ActionProxy
from project.server.main.objects.moduleimport import ModuleImportProxy
from project.server.main.objects.parameter import ParameterProxy

from project.server.main.objects.swift.swift_module import SwiftModule
from project.server.main.objects.swift.swift_module import SwiftState
from project.server.main.objects.swift.swift_module import SwiftAction
from project.server.main.objects.swift.swift_module import SwiftParameter
from project.server.main.objects.swift.swift_module import SwiftSubmodule

from project.server.main.objects.submodule import Submodule
from project.server.main.objects.moduleimport import ModuleImport
from project.server.main.objects.parameter import Parameter
from project.server.main.objects.action import Action
from project.server.main.objects.state import State

@dataclass
class SubmoduleProxy:
    pass

@dataclass
class ModuleProxy:
    name: str
    description: str
    extra_info = dict
    states: [StateProxy]
    actions: [ActionProxy]
    submodules: [SubmoduleProxy]
    module_imports: [ModuleImportProxy]
    
    def swift(self):
        return SwiftModule(
            name=self.name, 
            description=self.description, 
            extra_info=self.extra_info, 
            states=[
                SwiftState(
                    name=s.name,
                    attribute=s.extra_dict().get("attribute", ""),
                    simple_type=s.type,
                    private_default_value=s.extra_dict().get("default_value", ""),
                    access_control=s.access_control,
                    generic_of=s.extra_dict().get("generic_of", ""),
                    is_mutable=s.is_mutable,
                    is_optional=s.extra_dict().get("is_optional", ""),
                    is_generic_optional=s.extra_dict().get("default_value", ""),
                    extra_info=s.extra_dict(),
                    description=s.description
                ) 
                for s in self.states
            ], 
            actions=[
                SwiftAction(
                    name=a.name,
                    module_name=self.name,
                    extra_info=a.extra_dict(), 
                    parameters=[
                        SwiftParameter(
                            name=p.name, 
                            generic_of=p.extra_dict().get("generic_of", ""),
                            type=p.type,
                            is_generic_optional=p.extra_dict().get("is_generic_optional", ""), 
                            is_optional=p.extra_dict().get("is_optional", ""), 
                            index=i, 
                            extra_info=p.extra_dict()
                        )
                        for i ,p in enumerate(a.parameters)
                    ]
                ) 
                for a in self.actions 
            ], 
            submodules=[
                SwiftSubmodule(
                    name=sm.name, 
                    type=sm.type, 
                    presentation_type=sm.presentation_type, 
                    extra_info=sm.extra_dict()
                )
                for sm in self.submodules                
            ], 
            module_imports=self.module_imports
        )
    
    ## Takes SQLAlchemy object and converts it to a proxy
    def __init__(
            self, 
            name: str, 
            description: str, 
            states: [State], 
            actions: [Action], 
            submodules: [Submodule], 
            module_imports: [ModuleImport], 
            extra_info: dict
        ):
        self.name=name
        self.description=description
        self.extra_info=extra_info is not None and extra_info or dict()
        self.states=[
            StateProxy(
                access_control=s.access_control,
                is_mutable=s.is_mutable,
                name=s.name, 
                type=s.type,
                extra_info=s.extra_info is not None and extra_info or dict(), 
                description=s.description, 
            ) 
            for s in states
        ]
        self.actions=[
            ActionProxy(
                name=a.name,
                extra_info=a.extra_info is not None and a.extra_info or dict(),
                description=a.description,
                parameters=[ 
                    ParameterProxy(
                        name=p.name, 
                        type=p.type, 
                        extra_info=p.extra_dict()
                    ) 
                    for p in a.parameters 
                ]
            ) 
            for a in actions
        ]
        self.submodules=[ 
            SubmoduleProxy(
                name=sm.name, 
                type=sm.type, 
                reference=sm.reference, 
                extra_info=sm.extra_info is not None and sm.extra_info or dict(),
                presentation_type=sm.presentation_type
            ) 
            for sm in submodules 
        ]
        self.module_imports=[ 
            ModuleImportProxy(
                name=i.name, 
                function_name=i.function,
                extra_info=i.extra_info
            ) 
            for i in module_imports
        ]

@dataclass
class ModuleReferenceProxy:
    name: str
    description: str
    extra_info = dict
    states: [StateProxy]
    actions: [ActionProxy]
    submodules: [SubmoduleProxy]
    module_imports: [ModuleImportProxy]

    def __init__(self, module: ModuleProxy):
        self.name=module.name
        self.description=module.description
        self.extra_info=module.extra_info
        self.states=module.states
        self.actions=module.actions
        self.submodules=module.submodules
        self.module_imports=module.module_imports



@dataclass
class SubmoduleProxy:
    name: str
    type: str
    reference: ModuleReferenceProxy
    extra_info = dict
    presentation_type: SubmoduleType

    def __init__(self, name, type, reference, extra_info, presentation_type):
        self.name = name
        self.type = type
        self.reference = reference
        self.extra_info = extra_info
        self.presentation_type = presentation_type

    def __init__(self, name, type, reference: Module, extra_info, presentation_type):
        self.name = name
        self.type = type
        self.presentation_type=presentation_type
        self.reference = ModuleReferenceProxy(reference)
        self.extra_info = extra_info

    def extra_dict(self):
        return dict