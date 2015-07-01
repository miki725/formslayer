# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from django.conf.urls import include, patterns, url

from pdf.api import urlpatterns as pdf_urlpatterns


urlpatterns = patterns(
    '',
    url('^pdf/', include(pdf_urlpatterns)),
)
