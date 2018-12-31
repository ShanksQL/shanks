# -*- coding: utf-8 -*-
__author__ = "shanks"

from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)


@app.route('/')
def hello_world():
    return '洁总、天黑了~'


if __name__ == '__main__':
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run()
