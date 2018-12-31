# -*- coding: utf-8 -*-
__author__ = "shanks"

from flask import render_template
from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("index.html")


if __name__ == '__main__':
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run()
