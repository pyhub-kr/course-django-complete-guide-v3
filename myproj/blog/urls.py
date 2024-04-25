from django.urls import path, include
from . import views
from . import api

urlpatterns = []

urlpatterns_api_v1 = [
    path("", api.post_list, name="post_list"),
    path("<int:pk>/", api.post_detail, name="post_detail"),
    path("new/", api.post_new, name="post_new"),
]

urlpatterns += [
    path("api/", include((urlpatterns_api_v1, "api-v1"))),
]
