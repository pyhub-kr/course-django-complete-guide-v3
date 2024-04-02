from django.urls import path
from . import views

app_name = "photolog"

urlpatterns = [
    path("", views.index, name="index"),
]
