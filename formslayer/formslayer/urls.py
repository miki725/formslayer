# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib import admin

from . import api as api_urlpatterns


urlpatterns = patterns(
    '',

    url(r'^api/', include(api_urlpatterns, namespace='api')),

    # admin
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^{}(?P<path>.*)$'.format(settings.MEDIA_URL[1:]),
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )
