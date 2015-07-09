# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import pytest
from rest_framework.test import APIRequestFactory


@pytest.fixture
def drf_rf():
    """DRF RequestFactory instance"""
    return APIRequestFactory()
