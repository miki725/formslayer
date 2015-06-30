# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from django.http import HttpResponse
from rest_framework.authentication import (
    SessionAuthentication,
    TokenAuthentication,
)
from rest_framework.decorators import detail_route
from rest_framework.viewsets import ModelViewSet

from .models import PDFForm
from .permissions import IsOwnerPermission
from .serializers import FillFormSerializer, PDFFormSerializer


class PDFFormViewSet(ModelViewSet):
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
        return super(PDFFormViewSet, self).get_queryset().filter(owner_id=self.request.user.pk)

    @detail_route(methods=['post'])
    def fill(self, request, *args, **kwargs):
        self.object = self.get_object()

        serializer = FillFormSerializer(
            data=request.data,
            instance=self.object,
            context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)

        data = {i['name']: i['value'] for i in serializer.validated_data['fields']}
        pdf = self.object.fill(data)

        return HttpResponse(pdf, content_type='application/pdf')
