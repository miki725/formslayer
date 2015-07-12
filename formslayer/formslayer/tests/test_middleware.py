# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import mock

from formslayer.middleware import LoggerMiddleware


TESTING_MODULE = 'formslayer.middleware'


class TestLoggerMiddleware(object):
    @mock.patch(TESTING_MODULE + '.log')
    def test_process_request(self, mock_log):
        r = mock.Mock()
        assert LoggerMiddleware().process_request(r) is None
        assert r.log == mock_log.new.return_value
        mock_log.new.tassert_called_once_with(request_id=mock.ANY)
