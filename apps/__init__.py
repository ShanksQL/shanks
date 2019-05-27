# -*- coding: utf-8 -*-
__author__ = "shanks"

from flask import Flask
from .user import meet
from .circle import me
from .document import you
from .index import index


app = Flask(__name__)
app.register_blueprint(meet, url_prefix='/api/meet')
app.register_blueprint(you, url_prefix='/api/left')
app.register_blueprint(me, url_prefix='/api/right')
# app.register_blueprint(index, url_prefix='/api/index')
app.register_blueprint(index)
