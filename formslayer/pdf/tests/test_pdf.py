# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from subprocess import PIPE, SubprocessError

import mock
import pytest
from django.core.files.base import ContentFile

from pdf.exceptions import PDFNotFilled
from pdf.pdf import PDFFiller, tmp_file


TESTING_MODULE = 'pdf.pdf'


@mock.patch('os.unlink')
@mock.patch('os.fdopen')
@mock.patch('tempfile.mkstemp')
def test_tmp_file(mock_mksfile, mock_fdopen, mock_unlink):
    mock_mksfile.return_value = mock.sentinel.fid, mock.sentinel.path
    mock_fdopen.return_value.closed = False

    with tmp_file('wb', suffix='.foo') as fid:
        mock_mksfile.assert_called_once_with(
            suffix='.foo',
            prefix='tmp',
            dir=None
        )
        mock_fdopen.assert_called_once_with(mock.sentinel.fid, 'wb')

        assert fid == mock_fdopen.return_value
        assert fid.path == mock.sentinel.path
        assert not fid.close.called
        assert not mock_unlink.called

    fid.close.assert_called_once_with()
    mock_unlink.assert_called_once_with(mock.sentinel.path)


class TestPDFFiller(object):
    def test_init(self):
        pdf = PDFFiller(mock.sentinel.pdf, mock.sentinel.data, True)
        assert pdf.pdf == mock.sentinel.pdf
        assert pdf.data == mock.sentinel.data
        assert pdf.flatten

    def test_generate_fdf(self):
        pdf = PDFFiller(ContentFile(''), {'foo': 'bar'})

        fdf = pdf.generate_fdf()

        assert fdf == (
            b'<?xml version="1.0" encoding="UTF-8"?>'
            b'<xfdf xmlns="http://ns.adobe.com/xfdf/" xml:space="preserve">'
            b'<fields>'
            b'<field name="foo"><value>bar</value></field>'
            b'</fields>'
            b'</xfdf>'
        )

    @mock.patch(TESTING_MODULE + '.PDFTK_PATH', '/pdftk')
    @mock.patch(TESTING_MODULE + '.Popen')
    def test_call(self, mock_popen):
        mock_popen.return_value.communicate.return_value = 'stdout', 'stderr'
        mock_popen.return_value.returncode = 0
        pdf_file = mock.MagicMock()
        pdf = PDFFiller(pdf_file, {}, True)

        actual = pdf.call('/foo', '/bar')

        assert actual == 'stdout'
        mock_popen.assert_called_once_with(
            '/pdftk /bar fill_form /foo output - flatten',
            shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE
        )

    @mock.patch(TESTING_MODULE + '.PDFTK_PATH', '/pdftk')
    @mock.patch(TESTING_MODULE + '.Popen')
    def test_call_non_zero_return_code(self, mock_popen):
        mock_popen.return_value.communicate.return_value = 'stdout', 'stderr'
        mock_popen.return_value.returncode = 5
        pdf_file = mock.MagicMock()
        pdf = PDFFiller(pdf_file, {}, True)

        with pytest.raises(PDFNotFilled):
            pdf.call('/foo', '/bar')

    @mock.patch(TESTING_MODULE + '.PDFTK_PATH', '/pdftk')
    @mock.patch(TESTING_MODULE + '.Popen')
    def test_call_os_error(self, mock_popen):
        mock_popen.return_value.communicate.side_effect = SubprocessError
        pdf_file = mock.MagicMock()
        pdf = PDFFiller(pdf_file, {}, True)

        with pytest.raises(PDFNotFilled):
            pdf.call('/foo', '/bar')

    @mock.patch.object(PDFFiller, 'call')
    @mock.patch.object(PDFFiller, 'generate_fdf')
    @mock.patch(TESTING_MODULE + '.tmp_file')
    def test__call(self, mock_tmp_file, mock_generate_fdf, mock_call):
        pdf_file = mock.MagicMock()
        pdf = PDFFiller(pdf_file, {}, True)

        actual = pdf()

        assert actual == mock_call.return_value
        mock_tmp_file.assert_any_call('wb', suffix='.xfdf')
        mock_tmp_file.assert_any_call('wb', suffix='.pdf')
        mock_tmp_file().__enter__().write.assert_any_call(mock_generate_fdf.return_value)
        mock_tmp_file().__enter__().write.assert_any_call(pdf_file.read.return_value)
        mock_tmp_file().__enter__().close.assert_any_call()
