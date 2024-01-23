from django.urls import path
from . import views


urlpatterns = [
    path("travel/current/update/", views.current_travel_edit),
]
