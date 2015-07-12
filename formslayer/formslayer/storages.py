# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from compressor.storage import CompressorFileStorage
from storages.backends.s3boto import S3BotoStorage
from storages.utils import setting


class StaticS3BotoStorage(S3BotoStorage):
    custom_domain = setting('AWS_S3_STATIC_CUSTOM_DOMAIN')
    bucket_name = setting('AWS_STATIC_STORAGE_BUCKET_NAME')

    def __init__(self, *args, **kwargs):
        super(StaticS3BotoStorage, self).__init__(*args, **kwargs)
        self.local_storage = CompressorFileStorage()

    def save(self, name, content):
        name = super(StaticS3BotoStorage, self).save(name, content)
        self.local_storage._save(name, content)
        return name


class MediaS3BotoStorage(S3BotoStorage):
    custom_domain = setting('AWS_S3_MEDIA_CUSTOM_DOMAIN')
    bucket_name = setting('AWS_MEDIA_STORAGE_BUCKET_NAME')
