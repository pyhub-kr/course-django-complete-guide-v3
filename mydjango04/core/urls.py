# core/urls.py

from django.urls import path
from . import views

app_name = "core"  # URL Reverse를 위한 Namespace 지정

urlpatterns = [
    path("", views.index, name="index"),  # URL Reverse를 위한 URL Pattern명 지정
]
