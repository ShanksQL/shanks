# -*- coding: utf-8 -*-
__author__ = "shanks"

from apps import app
from werkzeug.contrib.fixers import ProxyFix


if __name__ == '__main__':
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run()
