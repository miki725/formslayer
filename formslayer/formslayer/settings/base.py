"""
Django settings for formslayer project.

This settings module is meant to contain all base configurations
for all other setting configurations.

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import os

import structlog


PROJECT_PATH = os.path.abspath(os.path.join(__file__, '..', '..'))
PROJECT_ROOT = os.path.dirname(PROJECT_PATH)
PROJECT_NAME = os.path.basename(PROJECT_PATH)

INSTALLED_APPS = [
    'pdf',

    'braces',
    'compressor',
    'djangosecure',
    'rest_framework',
    'rest_framework.authtoken',
    'storages',
    'vanilla',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE_CLASSES = [
    'formslayer.middleware.LoggerMiddleware',
    'djangosecure.middleware.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_auxilium.middleware.html.MinifyHTMLMiddleware',
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Media files
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')
MEDIA_URL = '/media/'

# Static files
STATIC_ROOT = os.path.join(PROJECT_PATH, 'all_static')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(PROJECT_PATH, 'static'),
]
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

SECRET_KEY = 'c*gbyuru7$wrxm438wl&p@movcvh$1^rl_*l0z6^(8x6n0qr=_'

# Templates
TEMPLATE_DIRS = [
    os.path.join(PROJECT_PATH, 'templates'),
]

# URLs
ROOT_URLCONF = 'formslayer.urls'
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/'
WSGI_APPLICATION = 'formslayer.wsgi.application'

# DRF
REST_FRAMEWORK = {
    'PAGE_SIZE': 100,
}

# django-compressor
COMPRESS_OFFLINE = False
COMPRESS_CSS_FILTERS = ['compressor.filters.yuglify.YUglifyCSSFilter']
COMPRESS_JS_FILTERS = ['compressor.filters.yuglify.YUglifyJSFilter']
COMPRESS_PRECOMPILERS = [
    ('text/less', 'lessc {infile} {outfile}'),
]

# logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s '
                      '%(levelname)s '
                      '%(name)s '
                      '%(message)s'
        },
        'simple': {
            'format': '%(levelname)s '
                      '%(name)s '
                      '%(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'null': {
            'level': 'INFO',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'pdf': {
            'level': 'INFO',
            'handlers': ['console'],
        }
    }
}

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(),
    ],
    context_class=structlog.threadlocal.wrap_dict(dict),
    logger_factory=structlog.stdlib.LoggerFactory(),
)
