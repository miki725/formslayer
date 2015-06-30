"""
WSGI config for formslayer project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "formslayer.settings.dev")

application = get_wsgi_application()
