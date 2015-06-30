# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from rest_framework import permissions


class IsOwnerPermission(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
