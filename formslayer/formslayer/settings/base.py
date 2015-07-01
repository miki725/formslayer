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
    'vanilla',
    'pipeline',
    'rest_framework.authtoken',
    'rest_framework',
    'pdf',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django_auxilium.middleware.html.MinifyHTMLMiddleware',
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
)
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

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

# Pipeline
PIPELINE_COMPILERS = (
    'pipeline.compilers.less.LessCompiler',
)
PIPELINE_CSS = {
    'bootstrap': {
        'source_filenames': [
            'lib/bootstrap/less/bootstrap.less',
        ],
        'output_filename': 'lib/bootstrap/bootstrap.css',
        'extra_context': {
            'media': 'screen',
        },
    },
    'login': {
        'source_filenames': [
            'account/less/login.less',
        ],
        'output_filename': 'account/css/login.css',
        'extra_context': {
            'media': 'screen',
        },
    },
    'errors': {
        'source_filenames': [
            'errors/less/errors.less',
        ],
        'output_filename': 'errors/css/errors.css',
        'extra_context': {
            'media': 'screen',
        },
    },
}
PIPELINE_JS = {
    'bootstrap': {
        'source_filenames': [
            'lib/jquery/jquery.min.js',
            'lib/bootstrap/js/affix.js',
            'lib/bootstrap/js/alert.js',
            'lib/bootstrap/js/button.js',
            'lib/bootstrap/js/carousel.js',
            'lib/bootstrap/js/collapse.js',
            'lib/bootstrap/js/dropdown.js',
            'lib/bootstrap/js/modal.js',
            'lib/bootstrap/js/popover.js',
            'lib/bootstrap/js/scrollspy.js',
            'lib/bootstrap/js/tab.js',
            'lib/bootstrap/js/tooltip.js',
            'lib/bootstrap/js/transition.js',
        ],
        'output_filename': 'lib/bootstrap/bootstrap.js',
    },
    'ie': {
        'source_filenames': [
            'lib/html5shiv/html5shiv.js',
            'lib/respond/respond.js',
        ],
        'output_filename': 'lib/ie.js',
    },
}
