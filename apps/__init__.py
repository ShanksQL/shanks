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
app.register_blueprint(meet, url_prefix='/api/meet')
app.register_blueprint(you, url_prefix='/api/left')
app.register_blueprint(me, url_prefix='/api/right')
app.register_blueprint(index, url_prefix='/api/index')
