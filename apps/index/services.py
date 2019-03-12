# -*- coding: utf-8 -*-
__author__ = "shanks"
from flask import Blueprint

home_page = Blueprint("index", __name__)


@home_page.route("/")
def get_user_info():
    return "洁总、明天早点到帮我买包子吧~"
