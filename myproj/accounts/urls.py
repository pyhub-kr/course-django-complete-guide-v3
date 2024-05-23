from django.urls import path, include
from . import views
from . import api

app_name = "accounts"


urlpatterns_api_v1 = [
    path("status/", api.status, name="status"),
]

urlpatterns = [
    path("api/", include((urlpatterns_api_v1, "api-v1"))),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.profile_edit, name="profile_edit"),
]
