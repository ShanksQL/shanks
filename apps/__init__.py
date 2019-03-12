# -*- coding: utf-8 -*-
__author__ = "shanks"

from flask import Flask
from pure_life import meet
from pure_me import me
from pure_you import you
from index import index
from flask_cache import Cache


cache = Cache()
app = Flask(__name__)
cache.init_app(app=app)
app.register_blueprint(meet)
app.register_blueprint(you)
app.register_blueprint(me)
app.register_blueprint(index)
