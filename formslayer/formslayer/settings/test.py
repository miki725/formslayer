"""
Settings to be used in development.
"""
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from .dev import *  # noqa

LOGGING['loggers']['django.request']['handlers'] = ['null']
LOGGING['loggers']['pdf']['handlers'] = ['null']
