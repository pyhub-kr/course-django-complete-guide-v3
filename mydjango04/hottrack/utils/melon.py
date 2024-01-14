import json
from typing import List, Dict
from urllib.parse import urlencode
from urllib.request import Request, urlopen


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
    ),
}


# Song 모델의 melon_uid 필드는 문자열 타입이었고, 이를 id 정수 타입으로 변경


def get_likes_dict(melon_uid_list: List[int]) -> Dict[int, int]:
    url = "https://www.melon.com/commonlike/getSongLike.json"
    params = urlencode(
        {
            # 정수는 문자열로 변환해야만 join이 가능합니다.
            "contsIds": ",".join(map(str, melon_uid_list)),
        }
    )

    url_with_params = url + "?" + params

    request = Request(url_with_params, headers=HEADERS)
    result = json.loads(urlopen(request).read())
    likes_dict = {int(song["CONTSID"]): song["SUMMCNT"] for song in result["contsLike"]}

    return likes_dict
