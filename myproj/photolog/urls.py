from django.urls import path
from . import views

app_name = "photolog"

urlpatterns = [
    path("", views.index, name="index"),
    path("new/", views.note_new, name="note_new"),
    path("<int:pk>/", views.note_detail, name="note_detail"),
    path("<int:pk>/edit/", views.note_edit, name="note_edit"),
    path("<int:note_pk>/comments/", views.comment_list, name="comment_list"),
    path("<int:note_pk>/comments/new/", views.comment_new, name="comment_new"),
    path(
        "<int:note_pk>/comments/<int:pk>/edit/", views.comment_edit, name="comment_edit"
    ),
]
