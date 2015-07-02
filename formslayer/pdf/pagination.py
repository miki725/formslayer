# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from rest_framework.pagination import PageNumberPagination

from .serializers import PDFFormSerializer


class FilledFormPageNumberPagination(PageNumberPagination):
    def paginate_queryset(self, queryset, request, view=None):
        self.view = view
        return (super(FilledFormPageNumberPagination, self)
                .paginate_queryset(queryset, request, view))

    def get_paginated_response(self, data):
        response = (super(FilledFormPageNumberPagination, self)
                    .get_paginated_response(data))

        form_serializer = PDFFormSerializer(
            instance=self.view.form,
            context=self.view.get_serializer_context()
        )

        key, value = response.data.popitem()
        response.data['form'] = form_serializer.data
        response.data[key] = value

        return response
