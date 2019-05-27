# -*- coding: utf-8 -*-
__author__ = "shanks"
from flask import Blueprint

home_page = Blueprint("index", __name__)


@home_page.route("/")
def get_user_info():
    return "白茶清欢无别事、我在等风也在等你"
