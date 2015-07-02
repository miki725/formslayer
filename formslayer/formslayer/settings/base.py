"""
Django settings for formslayer project.

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import os


PROJECT_PATH = os.path.abspath(os.path.join(__file__, '..', '..', '..'))
PROJECT_NAME = os.path.basename(PROJECT_PATH)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'braces',
    'django_extensions',
    'compressor',
    'rest_framework',
    'rest_framework.authtoken',
    'vanilla',

    'pdf',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_auxilium.middleware.html.MinifyHTMLMiddleware',
)

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Media files
MEDIA_ROOT = os.path.join(PROJECT_PATH, PROJECT_NAME, 'media')
MEDIA_URL = '/media/'

# Static files
STATIC_ROOT = os.path.join(PROJECT_PATH, PROJECT_NAME, 'all_static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, PROJECT_NAME, 'static'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# Templates
TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, PROJECT_NAME, 'templates'),
)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)


# URLs
ROOT_URLCONF = 'formslayer.urls'
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/'
WSGI_APPLICATION = 'formslayer.wsgi.application'

REST_FRAMEWORK = {
    'PAGE_SIZE': 100,
}

COMPRESS_OFFLINE = True
COMPRESS_CSS_FILTERS = ['compressor.filters.yuglify.YUglifyCSSFilter']
COMPRESS_JS_FILTERS = ['compressor.filters.yuglify.YUglifyJSFilter']
COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)
