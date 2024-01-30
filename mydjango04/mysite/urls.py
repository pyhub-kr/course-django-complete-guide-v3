# mysite/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path(settings.ADMIN_PREFIX, admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("blog/", include("blog.urls")),
    path("core/", include("core.urls")),
    path("hottrack/", include("hottrack.urls")),
    path("shop/", include("shop.urls")),
    path("weblog/", include("weblog.urls")),
    path("", RedirectView.as_view(pattern_name="hottrack:index")),
]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
