# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import multiprocessing


bind = '0.0.0.0:8888'
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
max_requests = 200
