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


def get_likes_dict(melon_uid_list: List[str]) -> Dict[str, int]:
    url = "https://www.melon.com/commonlike/getSongLike.json"
    params = urlencode(
        {
            "contsIds": ",".join(melon_uid_list),
        }
    )

    url_with_params = url + "?" + params

    request = Request(url_with_params, headers=HEADERS)
    result = json.loads(urlopen(request).read())
    likes_dict = {str(song["CONTSID"]): song["SUMMCNT"] for song in result["contsLike"]}

    return likes_dict
