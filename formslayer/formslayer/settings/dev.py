"""
Settings to be used in development.
"""
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from .base import *  # noqa


DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'formslayer.sqlite',
    }
}

INSTALLED_APPS += [
    'django_extensions',
]

ALLOWED_HOSTS = [
    '*',
]

LOGGING['loggers']['django.request']['level'] = 'DEBUG'
LOGGING['loggers']['pdf']['level'] = 'DEBUG'
