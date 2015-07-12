# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from functools import partial

import structlog
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status
from rest_framework.authentication import (
    SessionAuthentication,
    TokenAuthentication,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import FilledPDFForm, PDFForm
from .pagination import FilledFormPageNumberPagination
from .permissions import IsOwnerPermission
from .serializers import (
    FillFormSerializer,
    FilledPDFFormNestedSerializer,
    FilledPDFFormSerializer,
    PDFFormNestedSerializer,
)


log = structlog.get_logger()


class PDFFormViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    queryset = PDFForm.objects.all()
    serializer_class = PDFFormNestedSerializer

    authentication_classes = [
        TokenAuthentication,
        SessionAuthentication,
    ]
    permission_classes = [
        IsAuthenticated,
        IsOwnerPermission,
    ]

    def get_queryset(self):
        return (super(PDFFormViewSet, self).get_queryset()
                .filter(owner_id=self.request.user.pk))


class FilledPDFFormViewSet(mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.DestroyModelMixin,
                           GenericViewSet):
    queryset = FilledPDFForm.objects.select_related('form').all()
    serializer_class = FilledPDFFormSerializer
    serializer_nested_class = FilledPDFFormNestedSerializer

    authentication_classes = [
        TokenAuthentication,
        SessionAuthentication,
    ]
    permission_classes = [
        IsAuthenticated,
        partial(
            IsOwnerPermission,
            owner_getter=lambda i: hasattr(i, 'owner') and i.owner or i.form.owner
        ),
    ]
    pagination_class = FilledFormPageNumberPagination

    def get_form_queryset(self):
        return PDFForm.objects.filter(owner_id=self.request.user.pk)

    def get_queryset(self):
        self.form = get_object_or_404(
            self.get_form_queryset(),
            pk=self.kwargs['form_pk']
        )

        log.bind(owner=self.request.user.username, form=self.form)

        return (super(FilledPDFFormViewSet, self).get_queryset()
                .filter(form__owner_id=self.request.user.pk,
                        form_id=self.kwargs['form_pk']))

    def _is_request_to_detail(self):
        lookup = self.lookup_url_kwarg or self.lookup_field
        return lookup and lookup in self.kwargs

    def get_serializer_class(self):
        if any([self.paginator is None,
                self._is_request_to_detail()]):
            return self.serializer_nested_class
        else:
            return self.serializer_class

    def create(self, request, form_pk):
        # this sets self.form
        self.get_queryset()

        fill_serializer = FillFormSerializer(
            data=request.data,
            form=self.form,
            context=self.get_serializer_context()
        )
        fill_serializer.is_valid(raise_exception=True)

        filled_form = fill_serializer.save()

        serializer = self.get_serializer(instance=filled_form)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
