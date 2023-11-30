# mysite/urls.py
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.views.generic import RedirectView, TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("core/", include("core.urls")),
    # 최상위 주소에 대한 처리
    # #1. 템플릿 응답
    path("", TemplateView.as_view(template_name="root.html")),
    # #2. 다른 주소로 이동하기 (직접 URL 조합 방식)
    # path("", lambda request: redirect("/core/")),
    # path("", RedirectView.as_view(url="/core/")),
    # #2. 다른 주소로 이동하기 (URL Reverse 활용 방식)
    # path("", lambda request: redirect("core:index")),
    # path("", RedirectView.as_view(pattern_name="core:index")),
]
