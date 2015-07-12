# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import mock

from pdf.permissions import IsOwnerPermission


def test_init():
    perm = IsOwnerPermission()

    assert callable(perm.owner_getter)
    assert perm.owner_getter(
        mock.Mock(owner=mock.sentinel.owner)
    ) == mock.sentinel.owner


def test_has_object_permission(rf):
    r = rf.get('/')

    r.user = None
    assert not IsOwnerPermission().has_object_permission(
        r, None, mock.Mock(owner=mock.sentinel.owner)
    )

    r.user = mock.sentinel.owner
    assert IsOwnerPermission().has_object_permission(
        r, None, mock.Mock(owner=mock.sentinel.owner)
    )
