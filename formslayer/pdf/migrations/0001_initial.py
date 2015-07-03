# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid

import dirtyfields.dirtyfields
import django_auxilium.models.fields.files
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FilledPDFForm',
            fields=[
                ('id', models.UUIDField(serialize=False, default=uuid.uuid4, primary_key=True, editable=False)),
                ('filled_pdf', django_auxilium.models.fields.files.RandomFileField(upload_to='pdf/filled_forms')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='PDFForm',
            fields=[
                ('id', models.UUIDField(serialize=False, default=uuid.uuid4, primary_key=True, editable=False)),
                ('name', models.CharField(max_length=128)),
                ('pdf', django_auxilium.models.fields.files.RandomFileField(upload_to='pdf/forms')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(related_name='pdf_forms', to=settings.AUTH_USER_MODEL)),
            ],
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.AddField(
            model_name='filledpdfform',
            name='form',
            field=models.ForeignKey(related_name='filled_forms', to='pdf.PDFForm'),
        ),
    ]
