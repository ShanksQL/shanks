# -*- coding: utf-8 -*-
__author__ = "shanks"
__date__ = '2019/5/20 11:23 AM'

from gevent import monkey
import multiprocessing


monkey.patch_all()
debug = True
bind = '127.0.0.1:8080'
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gevent'
