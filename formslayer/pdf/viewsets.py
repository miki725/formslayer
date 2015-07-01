# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from functools import partial

from django.shortcuts import get_object_or_404
from rest_framework import mixins, status
from rest_framework.authentication import (
    SessionAuthentication,
    TokenAuthentication,
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import FilledPDFForm, PDFForm
from .permissions import IsOwnerPermission
from .serializers import (
    FillFormSerializer,
    FilledPDFFormSerializer,
    PDFFormSerializer,
)


class PDFFormViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    queryset = PDFForm.objects.all()
    serializer_class = PDFFormSerializer

    authentication_classes = [
        TokenAuthentication,
        SessionAuthentication,
    ]
    permission_classes = [
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

    authentication_classes = [
        TokenAuthentication,
        SessionAuthentication,
    ]
    permission_classes = [
        partial(IsOwnerPermission, owner_getter=lambda i: i.form.owner),
    ]

    def get_form_queryset(self):
        return PDFForm.objects.filter(owner_id=self.request.user.pk)

    def get_queryset(self):
        self.form = get_object_or_404(
            self.get_form_queryset(),
            pk=self.kwargs['form_pk']
        )

        return (super(FilledPDFFormViewSet, self).get_queryset()
                .filter(form__owner_id=self.request.user.pk,
                        form_id=self.kwargs['form_pk']))

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
