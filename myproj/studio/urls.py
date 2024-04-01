from django.urls import path
from . import views

app_name = "studio"

urlpatterns = [
    path("", views.index, name="index"),
    path("notes/new/", views.note_new, name="note_new"),
    path("notes/<int:pk>/", views.note_detail, name="note_detail"),
    path("notes/<int:pk>/edit/", views.note_edit, name="note_edit"),
    path("notes/<int:note_pk>/comments/", views.comment_list, name="comment_list"),
    path("notes/<int:note_pk>/comments/new/", views.comment_new, name="comment_new"),
    path(
        "notes/<int:note_pk>/comments/<int:pk>/edit/",
        views.comment_edit,
        name="comment_edit",
    ),
    path(
        "notes/<int:note_pk>/comments/<int:pk>/delete/",
        views.comment_delete,
        name="comment_delete",
    ),
]
