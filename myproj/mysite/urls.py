from django.apps import apps
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include

# from django_nextjs.render import render_nextjs_page


# async def root(request):
#     return await render_nextjs_page(request)


def test(request):
    return render(request, "test.html")


urlpatterns = [
    # path("", root),
    path("test/", test),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("blog/", include("blog.urls")),
    path("", include("photolog.urls")),
    path("", include("core.urls")),
    path("", include("django_components.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if apps.is_installed("debug_toolbar"):
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
