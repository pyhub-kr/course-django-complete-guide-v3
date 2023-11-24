from django.urls import path
from . import views

urlpatterns = [
    path(route="", view=views.index),
    path(route="export.csv", view=views.export_csv),
    path(route="<int:pk>/cover.png", view=views.cover_png),
]
