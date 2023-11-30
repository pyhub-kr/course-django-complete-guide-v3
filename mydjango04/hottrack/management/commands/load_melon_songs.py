# hottrack/management/commands/load_melon_songs.py

import json
from urllib.request import urlopen

from django.core.management import BaseCommand

from hottrack.models import Song


class Command(BaseCommand):
    help = "Load songs from melon chart"

    def handle(self, *args, **options):
        melon_chart_url = "https://raw.githubusercontent.com/pyhub-kr/dump-data/main/melon/melon-20230910.json"
        json_string = urlopen(melon_chart_url).read().decode("utf-8")

        # Song 인스턴스들은 아직 데이터베이스에 저장되지 않았습니다.
        song_list = [Song.from_dict(song_dict) for song_dict in json.loads(json_string)]
        print("loaded song_list :", len(song_list))

        # Song 인스턴스들은 한 번에 INSERT 쿼리를 생성하여, INSERT 성능을 높입니다.
        Song.objects.bulk_create(song_list, batch_size=100, ignore_conflicts=True)

        total = Song.objects.all().count()
        print("saved song_list :", total)
