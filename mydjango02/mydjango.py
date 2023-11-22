# mydjango.py

import sys
import django
import requests
from django.conf import settings
from django.core.management import execute_from_command_line
# from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path


settings.configure(
    ROOT_URLCONF=__name__,
    DEBUG=True,
    SECRET_KEY="secret",
    TEMPLATES=[
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": ["templates"],
        }
    ],
)
django.setup()


def index(request):
    json_url = "https://raw.githubusercontent.com/pyhub-kr/dump-data/main/melon/melon-20230906.json"

    response = requests.get(json_url)
    # response.raise_for_status()
    if response.ok:
        song_list = response.json()
    else:
        song_list = []

    # query = "Love"  # 검색어
    #
    # song_list = [
    #     {"곡명": "Seven (feat. Latto) - Clean Ver.", "가수": "정국"},
    #     {"곡명": "Love Lee", "가수": "AKMU (악뮤)"},
    #     {"곡명": "Super Shy", "가수": "NewJeans"},
    #     {"곡명": "후라이의 꿈", "가수": "AKMU (악뮤)"},
    #     {"곡명": "어떻게 이별까지 사랑하겠어, 널 사랑하는 거지", "가수": "AKMU (악뮤)"},
    # ]
    # # 파이썬 빌트인 함수 filter를 활용해서, 곡명에 검색어가 포함된 노래만 필터링
    # song_list = filter(lambda song: query in song["가수"] or query in song["곡명"], song_list)

    return render(request, "index.html", {"song_list": song_list})


urlpatterns = [
    path("", index),
]


execute_from_command_line(sys.argv)
