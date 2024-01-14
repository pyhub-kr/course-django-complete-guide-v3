# hottrack/management/commands/load_melon_songs.py

import json
from typing import List
from urllib.request import urlopen

from django.core.management import BaseCommand

from hottrack.models import Artist, Album, Genre, Song


# melon_chart_url = "https://raw.githubusercontent.com/pyhub-kr/dump-data/main/melon/melon-20230910.json"
# artist_uid, album_uid 필드가 추가되고, genre를 리스트화
DEFAULT_MELON_CHART_URL = "https://raw.githubusercontent.com/pyhub-kr/dump-data/main/melon/melon-20240114.json"


class Command(BaseCommand):
    help = "Load songs from melon chart"

    # 인자로 JSON 주소를 지정하지 않으면, 디폴트 주소를 활용
    def add_arguments(self, parser):
        parser.add_argument(
            "melon_chart_url", nargs="?", default=DEFAULT_MELON_CHART_URL
        )

    def handle(self, *args, **options):
        melon_chart_url = options["melon_chart_url"]

        json_string = urlopen(melon_chart_url).read().decode("utf-8")
        orig_song_list = json.loads(json_string)

        create_foreign_data(orig_song_list)

        # orig_song_list 내역을 토대로 데이터베이스에 없는 Song 레코드를 생성합니다.
        song_id_set = set(Song.objects.values_list("id", flat=True).distinct())

        song_list = []
        for song_dict in orig_song_list:
            song = Song.from_dict(song_dict)
            if song.id not in song_id_set:
                # 외래키 값으로 할당
                song.artist_id = song_dict["artist_uid"]
                song.album_id = song_dict["album_uid"]
                song._genre_name_list = song_dict["장르"]
                song_list.append(song)
                song_id_set.add(song.id)

        if song_list:
            print(f"{len(song_list)}개의 곡을 생성합니다.")
            Song.objects.bulk_create(song_list, batch_size=1000)

            for song in song_list:
                genre_qs = Genre.objects.filter(name__in=song._genre_name_list)
                song.genre_set.add(*genre_qs)
        else:
            print("새롭게 등록할 곡이 없습니다.")


def create_foreign_data(orig_song_list):
    """
    orig_song_list 내역을 토대로 데이터베이스에 없는 Artist/Album/Genre 레코드를 생성합니다.
    """

    artist_melon_uid_set = set(Artist.objects.values_list("id", flat=True).distinct())
    album_melon_uid_set = set(Album.objects.values_list("id", flat=True).distinct())
    genre_name_set = set(Genre.objects.values_list("name", flat=True).distinct())

    artist_list: List[Artist] = []
    album_list: List[Album] = []
    genre_list: List[Genre] = []

    for song_dict in orig_song_list:
        if song_dict["artist_uid"] not in artist_melon_uid_set:
            artist = Artist(
                id=song_dict["artist_uid"],
                name=song_dict["artist_name"],
            )
            artist_list.append(artist)
            artist_melon_uid_set.add(song_dict["artist_uid"])

        if song_dict["album_uid"] not in album_melon_uid_set:
            album = Album(
                id=song_dict["album_uid"],
                name=song_dict["album_name"],
            )
            album_list.append(album)
            album_melon_uid_set.add(song_dict["album_uid"])

        for genre_name in set(song_dict["장르"]) - genre_name_set:
            genre = Genre(name=genre_name)
            genre_list.append(genre)
            genre_name_set.update(song_dict["장르"])

    if artist_list:
        print(f"{len(artist_list)}개의 가수를 생성합니다.")
        Artist.objects.bulk_create(artist_list, batch_size=1000)
    else:
        print("새롭게 등록할 가수가 없습니다.")

    if album_list:
        print(f"{len(album_list)}개의 가수를 생성합니다.")
        Album.objects.bulk_create(album_list, batch_size=1000)
    else:
        print("새롭게 등록할 앨범이 없습니다.")

    if genre_list:
        print(f"{len(genre_list)}개의 장르를 생성합니다.")
        Genre.objects.bulk_create(genre_list, batch_size=1000)
    else:
        print("새롭게 등록할 장르가 없습니다.")
