from django.urls import path, include
from . import views
from . import api

urlpatterns = []

urlpatterns_api_v1 = []

urlpatterns += [
    path("api/", include((urlpatterns_api_v1, "api-v1"))),
]
