from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("posts/", views.post_list, name="post_list"),
    path("posts/new/", views.post_new, name="post_new"),
    path("posts/search/", views.search, name="search"),
    path(
        "posts/premium-user-guide/", views.premium_user_guide, name="premium_user_guide"
    ),
    path(
        "posts/premium/<str:slug>/",
        views.post_premium_detail,
        name="post_premium_detail",
    ),
    path("posts/<str:slug>/", views.post_detail, name="post_detail"),
    path("reviews/new/", views.review_new, name="review_new"),
]
