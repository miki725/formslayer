# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import mock
from compressor.storage import CompressorFileStorage
from storages.backends.s3boto import S3BotoStorage

from formslayer.storages import StaticS3BotoStorage


class TestStaticS3BotoStorage(object):
    def test_init(self):
        storage = StaticS3BotoStorage()

        assert isinstance(storage.local_storage, CompressorFileStorage)

    @mock.patch.object(S3BotoStorage, 'save')
    def test_save(self, mock_super_save):
        storage = StaticS3BotoStorage()
        storage.local_storage = mock.Mock()

        actual = storage.save(mock.sentinel.name, mock.sentinel.content)

        assert actual == mock_super_save.return_value
        mock_super_save.assert_called_once_with(
            mock.sentinel.name, mock.sentinel.content
        )
        storage.local_storage._save.assert_called_once_with(
            mock_super_save.return_value, mock.sentinel.content
        )
