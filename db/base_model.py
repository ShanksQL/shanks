# -*- coding: utf-8 -*-
__author__ = "shanks"
__date__ = '2019/6/11 9:27 AM'

from environment import Environment
from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base, AbstractConcreteBase, declared_attr


class_registry = {}
Base = declarative_base(class_registry=class_registry)


class BaseModel(AbstractConcreteBase, Base):
    """
    ORM Model基类，提供：
    1、id
    2、json
    3、利用dict update对象，受allowed_update_column约束
    """

    id = Column(Integer, primary_key=True)

    allowed_update_column = []

    def __repr__(self):
        return '<{}:{}>'.format(self.__class__.__name__, self.id)

    @classmethod
    def db(cls):
        return Environment().db

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
