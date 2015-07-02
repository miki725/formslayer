"""
Checklist for production-ready settings:
https://docs.djangoproject.com/en/dev/howto/deployment/checklist/
"""
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from ..utils import env
from .base import *  # noqa


DEBUG = False

ALLOWED_HOSTS = env('ALLOWED_HOSTS').split(',')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASSWORD'),
        'HOST': env('DATABASE_HOST'),
        'PORT': env('DATABASE_PORT', default='5432'),
    }
}

SECRET_KEY = env('SECRET_KEY')

MIDDLEWARE_CLASSES = [
    'breach_buster.middleware.gzip.GZipMiddleware',
] + MIDDLEWARE_CLASSES

DEFAULT_FILE_STORAGE = 'formslayer.storages.MediaS3BotoStorage'
COMPRESS_STORAGE = 'formslayer.storages.StaticS3BotoStorage'

AWS_ACCESS_KEY_ID = env('AWS_S3_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_S3_SECRET_ACCESS_KEY')
AWS_STATIC_STORAGE_BUCKET_NAME = env('AWS_S3_STATIC_STORAGE_BUCKET_NAME')
AWS_MEDIA_STORAGE_BUCKET_NAME = env('AWS_S3_MEDIA_STORAGE_BUCKET_NAME')

STATIC_URL = COMPRESS_URL = 'https://s3.amazonaws.com/{bucket}/'.format(bucket=AWS_STATIC_STORAGE_BUCKET_NAME)
MEDIA_URL = 'https://s3.amazonaws.com/{bucket}/'.format(bucket=AWS_MEDIA_STORAGE_BUCKET_NAME)

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = None  # added by nginx
SECURE_HSTS_INCLUDE_SUBDOMAINS = None  # added by nginx
SECURE_FRAME_DENY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = True

SECURE_CHECKS = [
    'djangosecure.check.csrf.check_csrf_middleware',
    'djangosecure.check.sessions.check_session_cookie_secure',
    'djangosecure.check.sessions.check_session_cookie_httponly',
    'djangosecure.check.djangosecure.check_security_middleware',
    # 'djangosecure.check.djangosecure.check_sts',
    'djangosecure.check.djangosecure.check_frame_deny',
    'djangosecure.check.djangosecure.check_content_type_nosniff',
    'djangosecure.check.djangosecure.check_xss_filter',
    'djangosecure.check.djangosecure.check_ssl_redirect',
]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_SUBJECT_PREFIX = env('EMAIL_SUBJECT_PREFIX', default='[formslayer] ')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True

COMPRESS_OFFLINE = True