
from datetime import datetime
import re
from project.server import db

from project.server.main.objects.enums import SubmoduleType, GeneratedSubmoduleRepresentation, GeneratedSubmoduleState
from jinja2 import Environment, Template, FileSystemLoader, BaseLoader

from project.server.main.objects.swift.swift_module import SwiftModule
from project.server.main.objects.codetemplate import CodeTemplate



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
    
    def swift(self) -> SwiftModule:
        return SwiftModule(module=self)

    def submodules_extra(self):
        stacks = []
        presentations = []
        results = []
        # for submodule in self.submodules:
        #     if submodule.presentation_type == SubmoduleType.Stack:
        #         stacks.append(GeneratedSubmoduleState(name=submodule.name,type=submodule.reference.name))
        #     if submodule.presentation_type == SubmoduleType.Presentation:
        #         presentations.append(GeneratedSubmoduleState(name=submodule.name,type=submodule.reference.name))

        # if len(stacks) > 0:
        #     results.append(GeneratedSubmoduleRepresentation(name="name",type="{}Destination".format(self.name),items=stacks))

        # if len(presentations) > 0:
        #     results.append(GeneratedSubmoduleRepresentation(name="name",type="{}Sheet".format(self.name),items=presentations))

        return results

    def swift_imports(self):
        result = ""
        for module_import in self.module_imports:
            result += "import {}\n".format(module_import.name)
        return result


    def swift_tca_submodules_state_repr(self):
        defaults = []
        lists =[]
        stacks = []
        presentations = []
        for submodule in self.submodules:
            if submodule.presentation_type == SubmoduleType.Default:
                defaults.append(submodule)
            if submodule.presentation_type == SubmoduleType.List:
                lists.append(submodule)
            if submodule.presentation_type == SubmoduleType.Stack:
                stacks.append(submodule)
            if submodule.presentation_type == SubmoduleType.Presentation:
                presentations.append(submodule)
        result = ""
        for df in defaults:
            result += "{}\n".format(df.as_swift_submodule_default_repr())
        
        for ls in lists:
            result += "{}\n".format(ls.as_swift_submodule_list_repr())

        if len(stacks) > 0:
            result += "{}\n".format(stacks[0].as_swift_submodule_stack_repr())
        if len(presentations) > 0:
            result += "{}\n".format(presentations[0].as_swift_submodule_presentation_repr())

        return result
    
    def swift_tca_submodules_init_body_repr(self):
        defaults = []
        lists =[]
        stacks = []
        presentations = []
        for submodule in self.submodules:
            if submodule.presentation_type == SubmoduleType.Default:
                defaults.append(submodule)
            if submodule.presentation_type == SubmoduleType.List:
                lists.append(submodule)
            if submodule.presentation_type == SubmoduleType.Stack:
                stacks.append(submodule)
            if submodule.presentation_type == SubmoduleType.Presentation:
                presentations.append(submodule)
        result = ""
        for df in defaults:
            result += "self.{name} = {name}\n".format(name=df.name)
        
        for ls in lists:
            result += "self.{name} = {name}\n".format(name=ls.name)

        if len(stacks) > 0:
            result += "self.path = path"
        if len(presentations) > 0:
            result += "self.sheet = sheet"

        return result
    
    def swift_tca_submodules_state_init_repr(self):
        defaults = []
        lists =[]
        stacks = []
        presentations = []
        for submodule in self.submodules:
            if submodule.presentation_type == SubmoduleType.Default:
                defaults.append(submodule)
            if submodule.presentation_type == SubmoduleType.List:
                lists.append(submodule)
            if submodule.presentation_type == SubmoduleType.Stack:
                stacks.append(submodule)
            if submodule.presentation_type == SubmoduleType.Presentation:
                presentations.append(submodule)
        result = ""
        for df in defaults:
            result += "{}\n".format(df.as_swift_init_parameter_repr())
        
        for ls in lists:
            result += "{}\n".format(ls.as_swift_init_parameter_repr())

        if len(stacks) > 0:
            result += "{}\n".format(stacks[0].as_swift_init_parameter_repr())
        if len(presentations) > 0:
            result += "{}\n".format(presentations[0].as_swift_init_parameter_repr())

        return result
    
    def swift_tca_submodules_actions_init_repr(self):
        defaults = []
        lists =[]
        stacks = []
        presentations = []
        for submodule in self.submodules:
            if submodule.presentation_type == SubmoduleType.Default:
                defaults.append(submodule)
            if submodule.presentation_type == SubmoduleType.List:
                lists.append(submodule)
            if submodule.presentation_type == SubmoduleType.Stack:
                stacks.append(submodule)
            if submodule.presentation_type == SubmoduleType.Presentation:
                presentations.append(submodule)
        result = ""
        for df in defaults:
            result += "{}\n".format(df.as_swift_tca_submodule_action_repr())
        
        for ls in lists:
            result += "{}\n".format(ls.as_swift_tca_submodule_action_repr())

        if len(stacks) > 0:
            result += "{}\n".format(stacks[0].as_swift_tca_submodule_action_repr())
        if len(presentations) > 0:
            result += "{}\n".format(presentations[0].as_swift_tca_submodule_action_repr())

        return result
    
    def swift_tca_submodules_func_definitions_repr(self):
        defaults = []
        lists =[]
        stacks = []
        presentations = []
        for submodule in self.submodules:
            if submodule.presentation_type == SubmoduleType.Default:
                defaults.append(submodule)
            if submodule.presentation_type == SubmoduleType.List:
                lists.append(submodule)
            if submodule.presentation_type == SubmoduleType.Stack:
                stacks.append(submodule)
            if submodule.presentation_type == SubmoduleType.Presentation:
                presentations.append(submodule)
        result = ""
        for df in defaults:
            result += "{} {{\n\t\treturn .none \n\t}}".format(df.swift_tca_func_definition_repr())
        
        for ls in lists:
            result += "{} {{\n\t\treturn .none \n\t}}".format(ls.swift_tca_func_definition_repr())
        if len(stacks) > 0:
            result += "{} {{\n\t\treturn .none \n\t}}".format(stacks[0].swift_tca_func_definition_repr())
        if len(presentations) > 0:
            result += "{} {{\n\t\treturn .none \n\t}}".format(presentations[0].swift_tca_func_definition_repr())

        return result
    
    def swift_tca_submodules_bodies_init_repr(self):
        defaults = []
        lists =[]
        stacks = []
        presentations = []
        for submodule in self.submodules:
            if submodule.presentation_type == SubmoduleType.Default:
                defaults.append(submodule)
            if submodule.presentation_type == SubmoduleType.List:
                lists.append(submodule)
            if submodule.presentation_type == SubmoduleType.Stack:
                stacks.append(submodule)
            if submodule.presentation_type == SubmoduleType.Presentation:
                presentations.append(submodule)
        result = "\t"
        for df in defaults:
            result += "{}\n".format(df.swift_tca_body_case_repr())
        
        for ls in lists:
            result += "{}\n".format(ls.swift_tca_body_case_repr())

        if len(stacks) > 0:
            result += "{}\n".format(stacks[0].swift_tca_body_case_repr())
        if len(presentations) > 0:
            result += "{}\n".format(presentations[0].swift_tca_body_case_repr())

        return result




    def as_swift_repr(self):
        if self.selected_template_id is not None:
            code_template = CodeTemplate.query.filter_by(id=self.selected_template_id).first()
        else:
            code_template = CodeTemplate.query.first()

        if code_template is not None:

            template = Environment(loader=BaseLoader()).from_string(code_template.content)
            # swift = SwiftModule(module=self)
            result = template.render(module=self)
            return result
        else:
            return "{}".format(self.selected_template_id)
    
    def submodules_tca_repr(self):

        defaults = []
        lists =[]
        stacks = []
        presentations = []
        for submodule in self.submodules:
            if submodule.presentation_type == SubmoduleType.Default:
                defaults.append(submodule)
            if submodule.presentation_type == SubmoduleType.List:
                lists.append(submodule)
            if submodule.presentation_type == SubmoduleType.Stack:
                stacks.append(submodule)
            if submodule.presentation_type == SubmoduleType.Presentation:
                presentations.append(submodule)
        result = ""
        for df in defaults:
            result += "{}\n\t\t".format(df.as_swift_tca_scopes_repr())
        
        for ls in lists:
            result += "{}\n\t\t".format(ls.as_swift_tca_scopes_repr())

        if len(stacks) > 0:
            result += "{}\n\t\t".format(stacks[0].as_swift_tca_scopes_repr())
        if len(presentations) > 0:
            result += "{}\n\t\t".format(presentations[0].as_swift_tca_scopes_repr())

        return result

