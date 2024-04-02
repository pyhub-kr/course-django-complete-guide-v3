# core/decorators.py

from functools import wraps
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse, ParseResult

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required as django_login_required
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django_htmx.http import HttpResponseClientRedirect


def login_required_hx(
    function=None,
    redirect_field_name=REDIRECT_FIELD_NAME,
    login_url=None,
):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            decorated_view_func = django_login_required(
                function=view_func,
                redirect_field_name=redirect_field_name,
                login_url=login_url,
            )

            response = decorated_view_func(request, *args, **kwargs)

            if isinstance(response, HttpResponseRedirect):
                resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)

                if request.htmx and resolved_login_url in response.url:
                    # /accounts/login/?next=/blog/tags/new/%3F_%3D1710826915601
                    # next_url: str = response.url
                    # request.htmx.current_url
                    # return HttpResponseClientRedirect(next_url)

                    # HTMX 요청을 한 주소가 next 인자로 포함된 URL
                    redirect_url: str = response.url
                    # HTMX 요청을 한 페이지의 주소
                    new_redirect_url: str = request.htmx.current_url

                    # next 인자가 포함된 URL에서 next 인자만 new_redirect_url 값으로 변경
                    parsed: ParseResult = urlparse(redirect_url)
                    query_dict: dict = parse_qs(parsed.query)
                    query_dict["next"] = [new_redirect_url]
                    new_query: str = urlencode(query_dict, doseq=True)
                    new_next_url = urlunparse(
                        (
                            parsed.scheme,
                            parsed.netloc,
                            parsed.path,
                            parsed.params,
                            new_query,
                            parsed.fragment,
                        )
                    )

                    return HttpResponseClientRedirect(new_next_url)

            return response

        return wrapper

    if function:
        return decorator(function)

    return decorator
