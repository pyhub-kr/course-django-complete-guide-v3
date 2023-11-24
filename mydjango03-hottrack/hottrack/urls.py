from django.urls import path, re_path
from . import views

urlpatterns = [
    path(route="", view=views.index),
    re_path(route=r"^export\.(?P<format>(csv|xlsx))$", view=views.export),
    path(route="<int:pk>/cover.png", view=views.cover_png),
]
