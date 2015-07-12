# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import mock

from pdf.serializers import FillFormSerializer


TESTING_MODULE = 'pdf.serializers'


class TestFillFormSerializer(object):
    def test_init(self):
        serializer = FillFormSerializer(form=mock.sentinel.form)

        assert serializer.form == mock.sentinel.form

    @mock.patch(TESTING_MODULE + '.ContentFile')
    @mock.patch(TESTING_MODULE + '.FilledPDFForm')
    @mock.patch(TESTING_MODULE + '.PDFFiller')
    def test_create(self, mock_pdf_filler, mock_filled_pdf_form, mock_content_file):
        form = mock.Mock(pk=mock.sentinel.pk)
        serializer = FillFormSerializer(form=form)

        data = {
            'fields': [
                {'name': 'foo', 'value': 'bar'},
            ]
        }
        actual = serializer.create(data)

        assert actual == mock_filled_pdf_form.objects.create.return_value
        mock_filled_pdf_form.objects.create.assert_called_once_with(
            form_id=mock.sentinel.pk,
            filled_pdf=mock_content_file.return_value
        )
        mock_pdf_filler.assert_called_once_with(form.pdf, {'foo': 'bar'})
        mock_content_file.assert_called_once_with(
            mock_pdf_filler.return_value.return_value, 'foo.pdf'
        )
