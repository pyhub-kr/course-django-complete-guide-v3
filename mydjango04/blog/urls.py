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
    path("reviews/", views.review_list, name="review_list"),
    path("reviews/new/", views.review_new, name="review_new"),
    path("reviews/<int:pk>/", views.review_detail, name="review_detail"),
    path("reviews/<int:pk>/edit/", views.review_edit, name="review_edit"),
]
