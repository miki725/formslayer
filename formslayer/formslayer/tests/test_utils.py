# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import os

import mock
import pytest

from formslayer.utils import env


@mock.patch.dict(os.environ, {'foo': 'stuff'})
def test_env():
    assert env('foo', default='bar') == 'stuff'


@mock.patch.dict(os.environ, {})
def test_env_error():
    with pytest.raises(KeyError):
        env('foo')


@mock.patch.dict(os.environ, {})
def test_env_default():
    assert env('foo', default='bar') == 'bar'
