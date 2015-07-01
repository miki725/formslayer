# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from django.conf.urls import include, patterns, url
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from .viewsets import FilledPDFFormViewSet, PDFFormViewSet


router = DefaultRouter()
router.register('forms', PDFFormViewSet, 'pdf-form')

root_router = NestedSimpleRouter(router, 'forms', lookup='form')
root_router.register('filled', FilledPDFFormViewSet, 'filled-pdf-form')

urlpatterns = patterns(
    '',
    url(r'^', include(router.urls)),
    url(r'^', include(root_router.urls)),
)
