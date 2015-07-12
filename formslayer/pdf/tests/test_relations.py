# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import mock
import pytest

from pdf.relations import MultiplePKsHyperlinkedIdentityField


class TestMultiplePKsHyperlinkedIdentityField(object):
    def test_init(self):
        field = MultiplePKsHyperlinkedIdentityField('foo')

        assert field.lookup_fields == ['pk']
        assert field.lookup_url_kwargs == ['pk']

    def test_init_assertion(self):
        with pytest.raises(AssertionError):
            MultiplePKsHyperlinkedIdentityField(
                'foo',
                lookup_fields=['pk'],
                lookup_url_kwargs=['pk', 'id'],
            )

    @mock.patch.object(MultiplePKsHyperlinkedIdentityField, 'get_queryset')
    def test_get_object(self, mock_get_queryset):
        field = MultiplePKsHyperlinkedIdentityField(
            'foo',
            lookup_fields=['one', 'two'],
            lookup_url_kwargs=['foo', 'bar'],
        )

        actual = field.get_object(None, None, {'foo': 'value', 'bar': 'other'})

        assert actual == mock_get_queryset.return_value.get.return_value
        mock_get_queryset.assert_called_once_with()
        mock_get_queryset.return_value.get.assert_called_once_with(
            one='value', two='other'
        )

    def test_get_url_no_obj_pk(self):
        field = MultiplePKsHyperlinkedIdentityField('foo')

        assert field.get_url(mock.Mock(pk=None), None, None, None) is None

    def test_get_url(self):
        field = MultiplePKsHyperlinkedIdentityField(
            'foo',
            lookup_fields=['one', 'two'],
            lookup_url_kwargs=['foo', 'bar'],
        )
        mock_reverse = field.reverse = mock.MagicMock()

        actual = field.get_url(
            mock.Mock(pk=1, one='value', two='here'),
            mock.sentinel.view_name,
            mock.sentinel.request,
            mock.sentinel.format,
        )

        assert actual == mock_reverse.return_value
        mock_reverse.assert_called_once_with(
            mock.sentinel.view_name,
            kwargs={'foo': 'value', 'bar': 'here'},
            request=mock.sentinel.request,
            format=mock.sentinel.format,
        )
