# -*- coding: utf-8 -*-
__author__ = "shanks"

from flask import Blueprint

you = Blueprint("you", __name__, url_prefix='/left')


@you.route("/")
def get_user_info():
    return "这是YOU"
