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

SECRET_KEY = 'c*gbyuru7$wrxm438wl&p@movcvh$1^rl_*l0z6^(8x6n0qr=_'

LOGGING['loggers']['django.request']['level'] = 'DEBUG'
LOGGING['loggers']['pdf']['level'] = 'DEBUG'
