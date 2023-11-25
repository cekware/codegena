from sqlalchemy.orm import relationship
from flask import current_app
from flask_login import UserMixin
from project.server import db
from datetime import datetime
from project.server import login
import enum
import os
from jinja2 import Environment, Template, FileSystemLoader, BaseLoader
from flask_login import current_user


def clone_model(model):
    """Clone an arbitrary sqlalchemy model object without its primary key values."""
    # Ensure the model’s data is loaded before copying.
    model.id

    table = model.__table__
    non_pk_columns = [k for k in table.columns.keys() if k not in table.primary_key]
    data = {c: getattr(model, c) for c in non_pk_columns}
    data.pop('id')
    return data
# model = Model(**model_dict)