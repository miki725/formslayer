# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import uuid

import six

from pdf.models import FilledPDFForm, PDFForm


def test_pdf_form_str(db, admin_user):
    form = PDFForm(
        id=uuid.UUID('11111111-2222-3333-4444-555555555555'),
        name='test',
        owner=admin_user,
    )

    assert six.text_type(form) == (
        '11111111-2222-3333-4444-555555555555 (test) by admin'
    )


def test_filled_pdf_form_str(db, admin_user):
    form = PDFForm(
        id=uuid.UUID('11111111-2222-3333-4444-555555555555'),
        name='test',
        owner=admin_user,
    )
    filled = FilledPDFForm(
        id=uuid.UUID('99999999-2222-3333-4444-555555555555'),
        form=form,
    )

    assert six.text_type(filled) == (
        '99999999-2222-3333-4444-555555555555 for '
        '<11111111-2222-3333-4444-555555555555 (test) by admin>'
    )


def test_filled_pdf_form_str_without_form():
    filled = FilledPDFForm(
        id=uuid.UUID('99999999-2222-3333-4444-555555555555'),
    )

    assert six.text_type(filled) == '99999999-2222-3333-4444-555555555555'
