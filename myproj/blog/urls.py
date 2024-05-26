from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from . import views
from . import api
from .api import PostModelViewSet, TodoViewSet

router = DefaultRouter()
router.register(prefix="posts", viewset=PostModelViewSet)
router.register(prefix="todos", viewset=TodoViewSet)


urlpatterns = [
    # path("", TemplateView.as_view(template_name="blog/index.html"), name="index"),
    path("", views.index, name="index"),
    path("whoami/", views.whoami, name="whoami"),
]
urlpatterns_api_v1 = []
urlpatterns_api_v1 += router.urls

# urlpatterns_api_v1 = [
#     path("", api.post_list, name="post_list"),
#     path("<int:pk>/", api.post_detail, name="post_detail"),
#     path("new/", api.post_list, name="post_new"),
#     path("<int:pk>/edit/", api.post_detail, name="post_edit"),
#     path("<int:pk>/delete/", api.post_detail, name="post_delete"),
# ]

urlpatterns += [
    path("api/", include((urlpatterns_api_v1, "api-v1"))),
]
