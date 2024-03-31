from django.urls import path
from . import views

app_name = "studio"

urlpatterns = [
    path("", views.index, name="index"),
    path("notes/new/", views.note_new, name="note_new"),
    path("notes/<int:pk>/", views.note_detail, name="note_detail"),
]
