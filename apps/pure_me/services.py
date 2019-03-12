# -*- coding: utf-8 -*-
__author__ = "shanks"

from flask import Blueprint

me = Blueprint("me", __name__, url_prefix='/right')


@me.route("/")
def get_user_info():
    return "这是ME"
