
from datetime import datetime
import os
from project.server import db
from flask_login import current_user
import re
from flask import current_app

from project.server.main.objects.codetemplate import CodeTemplate

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    name = db.Column(db.String(140), nullable=False)
    description = db.Column(db.String(1024))

    modules = db.relationship('Module', backref='project')
    templates = db.relationship('CodeTemplate', backref='project')

    extra_info = db.Column(db.String(2048))

    __table_args__ = (db.UniqueConstraint('user_id', 'name', name='unique_name_per_user'),)


    @classmethod
    def new_project(cls, user):
        name="NewProject"
        projects = Project.query.filter(Project.user_id == user.id, Project.name.like('NewProject%')).all()
        if len(projects) > 0:
            max_number = 0
            for project in projects:
                value = re.search(r'\d+', project.name)
                if not value:
                    value = "0"
                else:
                    value = value.group(0)
                number = int(value)
                if max_number < number:
                    max_number = number
            max_number += 1
            name = "{}{}".format(name, max_number)
        
        data_file = os.path.join(current_app.root_path, '../client/static/templates/readme/example1.txt')
        with open(data_file, 'r') as file:
            data = file.read()
        return Project(owner=user, name=name, description=data)
    
from dataclasses import dataclass
from project.server.main.objects.module import Module, ModuleProxy, SubmoduleProxy
from project.server.main.objects.codetemplate import CodeTemplate, CodeTemplateProxy
from project.server.main.objects.moduleimport import ModuleImport, ModuleImportProxy
from project.server.main.objects.state import StateProxy
from project.server.main.objects.action import ActionProxy
from project.server.main.objects.parameter import ParameterProxy
from project.server.main.objects.swift.swift_project import SwiftProject
from project.server.main.objects.swift.swift_module import SwiftModule
from project.server.main.objects.swift.swift_state import SwiftState
from project.server.main.objects.swift.swift_action import SwiftAction
from project.server.main.objects.swift.swift_parameter import SwiftParameter
from project.server.main.objects.swift.swift_submodule import SwiftSubmodule
from project.server.main.objects.swift.swift_module_import import SwiftModuleImport


@dataclass
class ProjectProxy:
    name: str
    description: str
    modules: list[ModuleProxy]
    templates = list[CodeTemplateProxy]
    extra_info = dict

    # Converts to Swift Proxy
    @property
    def swift(self) -> SwiftProject:
        return SwiftProject(
            name=self.name, 
            description=self.description, 
            modules=[ 
                SwiftModule(
                    name=m.name, 
                    description=m.description, 
                    extra_info=m.extra_info, 
                    states=[
                        SwiftState(
                            name=s.name, 
                            description=s.description, 
                            extra_info=s.extra_info, 
                            type=s.type, 
                            value=s.value
                        ) 
                        for s in m.states
                    ], 
                    actions=[
                        SwiftAction(
                            name=a.name,
                            extra_info=a.extra_info,
                            parameters=[ 
                                SwiftParameter(
                                    name=p.name, 
                                    type=p.type, 
                                    extra_info=p.extra_info
                                ) 
                                for p in a.parameters 
                            ]
                        )
                        for a in m.actions
                    ],
                    submodules=[ 
                        SwiftSubmodule(
                            name=s.name, 
                            type=s.type, 
                            reference=s.reference, 
                            extra_info=s.extra_info
                        ) 
                        for s in m.submodules 
                    ], 
                    module_imports=[ 
                        SwiftModuleImport(
                            name=i.name
                        ) 
                        for i in m.module_imports 
                    ]
                ) 
                for m in self.modules 
            ], 
            templates=self.templates, 
            extra_info=self.extra_info
        )
    # takes SQLAlchemy object and converts it to a proxy
    def __init__(self, name: str, description: str, modules: list[Module], templates: list[CodeTemplate], extra_info: dict):
        self.name = name
        self.description = description
        self.modules = [ 
            ModuleProxy(
                name=m.name, 
                description=m.description, 
                extra_info=m.extra_info, 
                states=[
                    StateProxy(
                        name=s.name, 
                        description=s.description, 
                        extra_info=s.extra_info, 
                        type=s.type,
                        access_control=s.access_control,
                        is_mutable=s.is_mutable
                    ) 
                    for s in m.states
                ], 
                actions=[
                    ActionProxy(
                        name=a.name,
                        extra_info=a.extra_info,
                        description=a.description,
                        parameters=[ 
                            ParameterProxy(
                                name=p.name, 
                                type=p.type, 
                                extra_info=p.extra_info
                            ) 
                            for p in a.parameters 
                        ]
                    ) 
                    for a in m.actions
                ],
                submodules=[ 
                    SubmoduleProxy(
                        name=s.name, 
                        type=s.type, 
                        reference=s.reference, 
                        extra_info=s.extra_info
                    ) 
                    for s in m.submodules 
                ], 
                module_imports=[ 
                    ModuleImportProxy(name=i.name) 
                    for i in m.module_imports
                ]
            ) 
            for m in modules 
        ]

        self.templates = [ 
            CodeTemplateProxy(
                name=t.name, 
                description=t.description, 
                extra_info=t.extra_info, 
                content=t.content
            ) 
            for t in templates 
        ]
        self.extra_info = extra_info

