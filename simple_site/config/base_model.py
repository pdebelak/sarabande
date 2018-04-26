from datetime import datetime

from flask_sqlalchemy import Model
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declared_attr


class BaseModel(Model):
    @declared_attr
    def id(cls):
        return Column(Integer, primary_key=True)

    @declared_attr
    def created_at(cls):
        return Column(DateTime, nullable=False, default=datetime.utcnow)

    @declared_attr
    def updated_at(cls):
        return Column(DateTime, nullable=False,
                      default=datetime.utcnow, onupdate=datetime.utcnow)
