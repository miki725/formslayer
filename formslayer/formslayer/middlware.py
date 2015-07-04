# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import uuid

import six
import structlog


log = structlog.get_logger()


class LoggerMidleware(object):
    def process_request(self, request):
        request.log = log.new(request_id=six.text_type(uuid.uuid4()))
