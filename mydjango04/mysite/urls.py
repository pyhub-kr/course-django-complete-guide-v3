# mysite/urls.py
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("core/", include("core.urls")),
    path("hottrack/", include("hottrack.urls")),
    path("", RedirectView.as_view(pattern_name="hottrack:index")),
]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
