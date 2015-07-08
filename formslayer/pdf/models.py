# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import uuid

import six
from dirtyfields import DirtyFieldsMixin
from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django_auxilium.models.fields import RandomFileField
from django_auxilium.models.signals import (
    file_field_auto_change_delete,
    file_field_auto_delete,
)


@file_field_auto_delete('pdf')
@file_field_auto_change_delete('pdf')
@python_2_unicode_compatible
class PDFForm(DirtyFieldsMixin, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='pdf_forms')
    name = models.CharField(max_length=128)
    pdf = RandomFileField(upload_to='pdf/forms')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            '{id} ({name}) by {owner}'
            ''.format(id=self.id, name=self.name, owner=self.owner)
        )


@file_field_auto_delete('filled_pdf')
@file_field_auto_change_delete('filled_pdf')
@python_2_unicode_compatible
class FilledPDFForm(DirtyFieldsMixin, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    form = models.ForeignKey(PDFForm, related_name='filled_forms')
    filled_pdf = RandomFileField(upload_to='pdf/filled_forms')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.form_id:
            return (
                '{id} for <{form}>'
                ''.format(id=self.id, form=six.text_type(self.form))
            )
        return six.text_type(self.id)
