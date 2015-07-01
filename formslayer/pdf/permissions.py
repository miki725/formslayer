# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import operator

from rest_framework import permissions


class IsOwnerPermission(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def __init__(self, owner_getter=None):
        if owner_getter is None:
            owner_getter = operator.attrgetter('owner')
        self.owner_getter = owner_getter

        super(IsOwnerPermission, self).__init__()

    def has_object_permission(self, request, view, obj):
        return self.owner_getter(obj) == request.user
