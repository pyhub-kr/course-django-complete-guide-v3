from django.urls import path
from . import views

app_name = "studio"

urlpatterns = [
    path("", views.index, name="index"),
    path("@<username>/", views.user_page, name="user_page"),
    path(
        "@<username>/follow/",
        views.user_follow,
        name="user_follow",
        kwargs={"action": "follow"},
    ),
    path(
        "@<username>/unfollow/",
        views.user_follow,
        name="user_unfollow",
        kwargs={"action": "unfollow"},
    ),
    path("notes/new/", views.note_new, name="note_new"),
    path("notes/<int:pk>/", views.note_detail, name="note_detail"),
    path("notes/<int:pk>/edit/", views.note_edit, name="note_edit"),
    path(
        "notes/<int:pk>/like/",
        views.note_like,
        name="note_like",
        kwargs={"action": "like"},
    ),
    path(
        "notes/<int:pk>/like/cancel/",
        views.note_like,
        name="note_like_cancel",
        kwargs={"action": "cancel"},
    ),
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
