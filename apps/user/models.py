# -*- coding: utf-8 -*-
__author__ = "shanks"

from db.base_model import BaseModel
from sqlalchemy import Column, String, Integer, DateTime, Boolean

# ========用户区域==========


class User(BaseModel):
    __table_name__ = 'user'
    name = Column(String(100), doc='姓名')
    mobile = Column(Integer, doc='手机号')
    gender = Column(String(50), doc='性别')
    birthday = Column(DateTime, doc='出生日期')
    create_data = Column(DateTime, doc='注册日期')
    enable = Column(Boolean, doc='是否注销')
    sign = Column(String(1000), doc='个性签名')


# ========圈子区域==========

class Circle(BaseModel):
    __table_name__ = 'circle'
    name = Column(String(100), doc='圈子名称')
    describe = Column(String(1000), doc='圈子描述')


class CircleNumber(BaseModel):
    __table_name__ = 'circle_number'
    category_id = Column(Integer, doc='圈子ID')
    user_id = Column(Integer, doc='成员ID')
    member_name = Column(String, doc='群昵称')
    enable = Column(Boolean, doc='是否生效')


# ========文件区域==========

class Document(BaseModel):
    __table_name__ = 'document'
    index = Column(String(100), doc='文件索引')
    name = Column(String(100), doc='文件名')
    file_type = Column(String(100), doc='文件类型')
    create_data = Column(DateTime, doc='上传时间')
    modify_data = Column(DateTime, doc='更新时间')
    describe = Column(String(1000), doc='描述')
    create_id = Column(Integer, doc='创建者ID')
    enable = Column(Boolean, doc='是否生效')
