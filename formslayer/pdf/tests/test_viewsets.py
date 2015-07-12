# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import mock
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from pdf.serializers import (
    FillFormSerializer,
    FilledPDFFormNestedSerializer,
    FilledPDFFormSerializer,
)
from pdf.viewsets import FilledPDFFormViewSet, PDFFormViewSet


TESTING_MODULE = 'pdf.viewsets'


class TestPDFFormViewSet(object):
    @mock.patch.object(GenericViewSet, 'get_queryset')
    def test_get_queryset(self, mock_super_get_queryset):
        request = mock.Mock()
        viewset = PDFFormViewSet(request=request)

        actual = viewset.get_queryset()

        assert actual == mock_super_get_queryset.return_value.filter.return_value
        mock_super_get_queryset.return_value.filter.assert_called_once_with(
            owner_id=request.user.pk
        )


class TestFilledPDFFormViewSet(object):
    @mock.patch(TESTING_MODULE + '.PDFForm')
    def test_get_form_queryset(self, mock_pdf_form):
        request = mock.Mock()
        viewset = FilledPDFFormViewSet(request=request)

        actual = viewset.get_form_queryset()

        assert actual == mock_pdf_form.objects.filter.return_value
        mock_pdf_form.objects.filter.assert_called_once_with(
            owner_id=request.user.pk
        )

    @mock.patch(TESTING_MODULE + '.get_object_or_404')
    @mock.patch.object(FilledPDFFormViewSet, 'get_form_queryset')
    @mock.patch.object(GenericViewSet, 'get_queryset')
    def test_queryset(self, mock_super_get_queryset, mock_get_form_queryset, mock_get_object_or_404):
        request = mock.Mock()
        viewset = FilledPDFFormViewSet(request=request, kwargs={'form_pk': 123})

        actual = viewset.get_queryset()

        assert actual == mock_super_get_queryset.return_value.filter.return_value
        assert viewset.form == mock_get_object_or_404.return_value
        mock_super_get_queryset.return_value.filter.assert_called_once_with(
            form__owner_id=request.user.pk,
            form_id=123
        )
        mock_get_form_queryset.assert_called_once_with()
        mock_get_object_or_404.assert_called_once_with(
            mock_get_form_queryset.return_value,
            pk=123
        )

    def test_get_serializer_class_detail(self):
        viewset = FilledPDFFormViewSet(kwargs={'pk': 123})

        actual = viewset.get_serializer_class()

        assert actual is FilledPDFFormNestedSerializer

    def test_get_serializer_class_detail_not_paginated(self):
        viewset = FilledPDFFormViewSet(_paginator=None, kwargs={})

        actual = viewset.get_serializer_class()

        assert actual is FilledPDFFormNestedSerializer

    def test_get_serializer_class_simple_serializer(self):
        viewset = FilledPDFFormViewSet(_paginator=True, kwargs={})

        actual = viewset.get_serializer_class()

        assert actual is FilledPDFFormSerializer

    @mock.patch.object(FillFormSerializer, 'save')
    @mock.patch.object(FilledPDFFormViewSet, 'get_serializer')
    @mock.patch.object(FilledPDFFormViewSet, 'get_queryset')
    def test_create(self, mock_get_queryset, mock_get_serializer, mock_save):
        request = mock.Mock(data={
            'fields': [
                {'name': 'foo', 'value': 'bar'}
            ]
        })
        form = mock.Mock()
        mock_get_serializer.return_value = mock.Mock(
            data={'url': '/uri/here', 'foo': 'bar'}
        )
        viewset = FilledPDFFormViewSet(
            request=request, form=form, format_kwarg=None, kwargs={},
        )

        actual = viewset.create(request, 123)

        assert isinstance(actual, Response)
        assert actual.data == {'url': '/uri/here', 'foo': 'bar'}
        assert actual.status_code == 201
        assert actual['Location'] == '/uri/here'
        mock_get_serializer.assert_called_once_with(instance=mock_save.return_value)
