# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from rest_framework.routers import DefaultRouter

from pdf.viewsets import PDFFormViewSet


router = DefaultRouter()
router.register('pdf/forms', PDFFormViewSet, 'pdf-forms')
urlpatterns = router.urls
