from datetime import datetime
import re
from project.server import db
from project.server.main.objects.enums import SubmoduleType

class Submodule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))
    is_optional = db.Column(db.Boolean, default=False)
    description = db.Column(db.String(1024))
    # name, type, parent_module_name

    # Default
    # public var {name}: {type}.State? = nil
    # List
    # public var {name}: IdentifiedArrayOf<{name}.State>
    # Stack
    # public var path: StackState<{parent_module_name}Destination.State> = .init()
    # Presentation
    # @PresentationState public var sheet: {parent_module_name}Sheet.State?

    name = db.Column(db.String(140), nullable=False)
    type = db.Column(db.String(140))
    presentation_type = db.Column(db.Enum(SubmoduleType), nullable=False, default=SubmoduleType.Default)
    default_value = db.Column(db.String(140))

    # 1-to-1 relationship called 'reference' to Module
    reference_id = db.Column(db.Integer, db.ForeignKey('module.id'))
    reference = db.relationship('Module', backref=db.backref('submodule_reference', uselist=False), foreign_keys=[reference_id])

    extra_info = db.Column(db.String(2048))
    __table_args__ = (db.UniqueConstraint('module_id', 'name', name='unique_submodule_name_per_module'),)

    @classmethod
    def new_submodule(cls, module, presentation_type):
        name="newSubmodule"
        submodules = Submodule.query.filter(Submodule.module_id == module.id, Submodule.name.like('newSubmodule%')).all()
        if len(submodules) > 0:
            max_number = 0
            for submodule in submodules:
                value = re.search(r'\d+', submodule.name)
                if not value:
                    value = "0" 
                else:
                    value = value.group(0)
                number = int(value)
                if max_number < number:
                    max_number = number
            max_number += 1
            name = "{}{}".format(name, max_number)


        type = ""
        is_optional = False
        default_value = ""
        if presentation_type == SubmoduleType.Default:
            type = "{}".format(module.name)
        if presentation_type == SubmoduleType.List:
            type = "{}".format(module.name)
            default_value = "[]"
        if presentation_type == SubmoduleType.Stack:
            type = "{}".format(module.name)
            default_value = ".init()"
        if presentation_type == SubmoduleType.Presentation:
            type = "{}".format(module.name)
            default_value = "nil"
            is_optional = True
        # basedir = os.path.abspath(os.path.dirname(__file__))
        # data_file = os.path.join(basedir, '../../client/static/templates/readme/example1.txt')
        # with open(data_file, 'r') as file:
        #     data = file.read()
     
        return Submodule(module=module, name=name, type=type, presentation_type=presentation_type, is_optional=is_optional, default_value=default_value)
    



