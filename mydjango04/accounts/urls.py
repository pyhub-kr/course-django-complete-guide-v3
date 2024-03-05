from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("profile/edit/", views.profile_edit, name="profile_edit"),
    path("profile/wizard/", views.profile_wizard, name="profile_wizard"),
    path("login/", views.login, name="login"),
    path("profile/", views.profile, name="profile"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.logout, name="logout"),
    path("password_change/", views.password_change, name="password_change"),
    path("password_reset/", views.password_reset, name="password_reset"),
    path(
        "reset/<uidb64>/<token>/",
        views.password_reset_confirm,
        name="password_reset_confirm",
    ),
]
