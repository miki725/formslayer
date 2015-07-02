# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from django.core.files.storage import get_storage_class
from storages.backends.s3boto import S3BotoStorage
from storages.utils import setting


class StaticS3BotoStorage(S3BotoStorage):
    bucket_name = setting('AWS_STATIC_STORAGE_BUCKET_NAME')


class MediaS3BotoStorage(S3BotoStorage):
    bucket_name = setting('AWS_MEDIA_STORAGE_BUCKET_NAME')

    def __init__(self, *args, **kwargs):
        super(MediaS3BotoStorage, self).__init__(*args, **kwargs)
        self.local_storage = get_storage_class('compressor.storage.CompressorFileStorage')()

    def save(self, name, content):
        name = super(MediaS3BotoStorage, self).save(name, content)
        self.local_storage._save(name, content)
        return name
