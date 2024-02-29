from django.urls import path
from . import views

app_name = "cafe"

urlpatterns = [
    path("", views.coffee_stamp, name="coffee_stamp"),
    path("free-coffee/", views.coffee_free, name="coffee_free"),
]
