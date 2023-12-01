from django.urls import path, re_path
from . import converters  # noqa
from . import views

urlpatterns = [
    path(route="", view=views.index),
    path(route="<int:pk>/", view=views.song_detail),
    path(route="melon-<int:melon_uid>/", view=views.song_detail),
    path(route="archives/<date:release_date>/", view=views.index),
    re_path(route=r"^export\.(?P<format>(csv|xlsx))$", view=views.export),
    path(route="<int:pk>/cover.png", view=views.cover_png),
]
