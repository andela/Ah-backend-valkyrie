from rest_framework import pagination
from rest_framework.response import Response

class ArticlePagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'articlesCount': self.page.paginator.count,
            'articles': data
        })