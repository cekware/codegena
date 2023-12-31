from datetime import datetime
import re
from project.server import db

class ModuleImport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), nullable=False)
    function = db.Column(db.String(140))
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))

    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    extra_info = db.Column(db.String(2048))
    description = db.Column(db.String(1024))
    @classmethod
    def new_module_import(cls, module):
        name="NewLibrary"
        modules = ModuleImport.query.filter(ModuleImport.module_id == module.id, ModuleImport.name.like('NewLibrary%')).all()
        if len(modules) > 0:
            max_number = 0
            for m in modules:
                value = re.search(r'\d+', m.name)
                if not value:
                    value = "0"
                else:
                    value = value.group(0)
                number = int(value)
                if max_number < number:
                    max_number = number
            max_number += 1
            name = "{}{}".format(name, max_number)
     
        return ModuleImport(name=name, module=module)
    
from dataclasses import dataclass

@dataclass
class ModuleImportProxy:
    name: str
    function_name: str
    extra_info = dict

    def __init__(self, name, function_name, extra_info):
        self.name = name
        self.function_name = function_name
        self.extra_info = extra_info