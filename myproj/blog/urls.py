from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.index, name="index"),
    path("friend_list/", views.friend_list, name="friend_list"),
    path("new_friend_list/", views.new_friend_list, name="new_friend_list"),
]
