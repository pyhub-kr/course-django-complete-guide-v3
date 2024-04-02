from django.urls import path
from . import views

app_name = "photolog"

urlpatterns = [
    path("", views.index, name="index"),
    path("new/", views.note_new, name="note_new"),
    path("<int:pk>/", views.note_detail, name="note_detail"),
]
