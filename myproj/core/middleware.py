# core/middleware.py

from typing import Callable
from urllib.parse import urlencode

from django.http import HttpRequest, HttpResponse


class SortQueryParamsMiddleware:
    """
    요청 URL의 쿼리 파라미터를 정렬하는 미들웨어
    """

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if request.GET:
            request.META["QUERY_STRING"] = urlencode(
                sorted(request.GET.items())  # noqa
            )

        response = self.get_response(request)
        return response
