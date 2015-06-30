# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from rest_framework import fields, serializers

from .models import PDFForm


class FillFormFieldSerializer(serializers.Serializer):
    name = fields.RegexField(regex=r'[\w\d]+', min_length=1, max_length=50)
    value = fields.CharField(max_length=2000)


class FillFormSerializer(serializers.Serializer):
    fields = FillFormFieldSerializer(many=True)


class PDFFormSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:pdf-forms-detail')
    id = fields.UUIDField(format='hex')

    class Meta(object):
        model = PDFForm
        fields = ['url', 'id', 'path']
