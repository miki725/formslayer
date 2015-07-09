# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import mock
from rest_framework.response import Response

from pdf.models import PDFForm
from pdf.pagination import FilledFormPageNumberPagination


def test_paginate_queryset(db, drf_rf):
    paginator = FilledFormPageNumberPagination()

    r = drf_rf.get('/')
    r.query_params = {}

    paginated = paginator.paginate_queryset(
        PDFForm.objects.all(),
        request=r,
        view=mock.sentinel.view,
    )

    assert isinstance(paginated, list)
    assert paginator.view == mock.sentinel.view


def test_get_paginated_reponse(db, drf_rf):
    data = [
        {'hello': 'world'},
        {'hello': 'mars'},
    ]
    paginator = FilledFormPageNumberPagination()

    r = drf_rf.get('/')
    r.query_params = {}

    paginator.paginate_queryset(
        PDFForm.objects.all(),
        request=r,
        view=mock.Mock(
            form=PDFForm(),
            pagination_serializer_class=None,
            paginate_by=10
        ),
    )

    response = paginator.get_paginated_response(data)

    assert isinstance(response, Response)
    assert list(response.data.keys()) == ['count', 'next', 'previous', 'form', 'results']
    assert isinstance(response.data['form'], dict)
