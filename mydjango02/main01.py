import requests  # pip install requests
from pprint import pprint  # 가독성좋게 출력하기 위한 모듈

json_url = "https://raw.githubusercontent.com/pyhub-kr/dump-data/main/melon/melon-20230906.json"

response = requests.get(json_url)
response.raise_for_status()  # 비정상 응답을 받았다면, HTTPError를 발생시킵니다.

song_list = response.json()

print(type(song_list), len(song_list), type(song_list[0]))
pprint(song_list)
