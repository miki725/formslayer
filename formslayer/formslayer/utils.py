# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import os


ENV_PREFIX = os.environ.get('ENV_PREFIX', 'FORMSLAYER_')


def env(key, **kwargs):
    try:
        return os.environ[ENV_PREFIX + key]
    except KeyError:
        if 'default' in kwargs:
            return kwargs['default']
        raise
