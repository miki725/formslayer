# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import uuid

from dirtyfields import DirtyFieldsMixin
from django.conf import settings
from django.db import models
from django_auxilium.models.fields import RandomFileField
from django_auxilium.models.signals import (
    file_field_auto_change_delete,
    file_field_auto_delete,
)

from .pdf import PDFFiller


@file_field_auto_delete('pdf')
@file_field_auto_change_delete('pdf')
class PDFForm(DirtyFieldsMixin, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='pdf_forms')
    pdf = RandomFileField(upload_to='pdf/forms')

    def fill(self, data, flatten=False):
        assert isinstance(data, dict)

        return PDFFiller(self.pdf.path, data, flatten)()
