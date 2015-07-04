# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import structlog
from django.core.files.base import ContentFile
from rest_framework import fields, serializers

from .models import FilledPDFForm, PDFForm
from .pdf import PDFFiller
from .relations import MultiplePKsHyperlinkedIdentityField


log = structlog.get_logger()


class FillFormFieldSerializer(serializers.Serializer):
    name = fields.RegexField(regex=r'[\w\d]+', min_length=1, max_length=50)
    value = fields.CharField(max_length=2000)


class FillFormSerializer(serializers.Serializer):
    fields = FillFormFieldSerializer(many=True)

    def __init__(self, *args, **kwargs):
        self.form = kwargs.pop('form', None)
        super(FillFormSerializer, self).__init__(*args, **kwargs)

    def create(self, validated_data):
        data = {i['name']: i['value'] for i in validated_data['fields']}

        pdf_data = PDFFiller(self.form.pdf, data)()
        pdf = ContentFile(pdf_data, 'foo.pdf')

        filled_in_pdf = FilledPDFForm.objects.create(
            form_id=self.form.pk,
            filled_pdf=pdf,
        )

        log.info('Created filled in PDF',
                 filled_in_pdf=filled_in_pdf,
                 filled_in_pdf_name=filled_in_pdf.filled_pdf.name)

        return filled_in_pdf


class PDFFormSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:pdf-form-detail')
    id = fields.UUIDField(format='hex', read_only=True)

    class Meta(object):
        model = PDFForm
        fields = ['url', 'id', 'name', 'pdf', 'created']
        read_only_fields = ['pdf', 'created']


class PDFFormNestedSerializer(PDFFormSerializer):
    filled = serializers.HyperlinkedIdentityField(
        view_name='api:filled-pdf-form-list',
        lookup_field='pk',
        lookup_url_kwarg='form_pk',
    )

    class Meta(PDFFormSerializer.Meta):
        fields = PDFFormSerializer.Meta.fields + ['filled']


class FilledPDFFormSerializer(serializers.ModelSerializer):
    url = MultiplePKsHyperlinkedIdentityField(
        view_name='api:filled-pdf-form-detail',
        lookup_fields=['form_id', 'pk'],
        lookup_url_kwargs=['form_pk', 'pk']
    )
    id = fields.UUIDField(format='hex', read_only=True)
    form = serializers.HyperlinkedIdentityField(
        view_name='api:pdf-form-detail',
        lookup_field='form_id',
        lookup_url_kwarg='pk',
    )

    class Meta(object):
        model = FilledPDFForm
        fields = ['url', 'id', 'form', 'filled_pdf', 'created']
        read_only_fields = ['form', 'filled_pdf', 'created']


class FilledPDFFormNestedSerializer(FilledPDFFormSerializer):
    form = PDFFormSerializer(read_only=True)
