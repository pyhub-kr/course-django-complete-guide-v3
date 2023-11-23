from django.conf import settings
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path(route="hottrack/", view=include("hottrack.urls")),
    path(route="", view=lambda request: redirect("/hottrack/")),
]

if settings.DEBUG:
    urlpatterns += [
        path(route="__debug__/", view=include("debug_toolbar.urls")),
    ]
