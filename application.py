# -*- coding: utf-8 -*-
__author__ = "shanks"

from apps import app
from werkzeug.middleware.proxy_fix import ProxyFix
import redis


def connect_redis():
    _redis_address = 'redis://127.0.0.1:6379'
    redis.StrictRedis.from_url(_redis_address)


def start_app():
    # connect_redis()
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run()


if __name__ == '__main__':
    start_app()
