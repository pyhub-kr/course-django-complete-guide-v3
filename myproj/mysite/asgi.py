# mysite/asgi.py

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.apps.registry import apps
from django.core.asgi import get_asgi_application
from django.urls import re_path, path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

django_asgi_app = get_asgi_application()


http_routes = [
    re_path(r"", django_asgi_app),
]
websocket_routes = []


if apps.is_installed("django_nextjs"):
    from django_nextjs.proxy import (
        NextJSProxyHttpConsumer,
        NextJSProxyWebsocketConsumer,
    )

    # Next.js 빌드 파일, 내부 API 엔드포인트, 로고 이미지 등의 주소 패턴
    #  - ?: 는 패턴을 찾지만, 그룹으로 캡처하진 않습니다.
    route = r"^(?:_next|__next|next|vercel.svg).*"
    view = NextJSProxyHttpConsumer.as_asgi()
    nextjs_proxy_path = re_path(route, view)
    http_routes.insert(0, nextjs_proxy_path)

    # HMR (Hot module replacement)을 위한 웹소켓 요청을 Next.js 서버로 전달
    hmr_route = "_next/webpack-hmr"
    hmr_view = NextJSProxyWebsocketConsumer.as_asgi()
    hmr_path = path(hmr_route, hmr_view)
    websocket_routes.append(hmr_path)


application = ProtocolTypeRouter(
    {
        "http": URLRouter(http_routes),
        "websocket": URLRouter(websocket_routes),
    }
)
