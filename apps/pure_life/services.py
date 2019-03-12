# -*- coding: utf-8 -*-
__author__ = "shanks"
from flask import Blueprint
meet = Blueprint("user", __name__, url_prefix='/meet')


@meet.route("/")
def get_user_info():
    return "这里是MEET"
