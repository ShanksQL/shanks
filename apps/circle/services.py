# -*- coding: utf-8 -*-
__author__ = "shanks"

from flask import Blueprint

me = Blueprint("me", __name__)


@me.route("/")
def get_user_info():
    return "这是ME"
