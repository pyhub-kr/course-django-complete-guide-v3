# core/renderers.py

from io import BytesIO

from rest_framework.renderers import BaseRenderer, JSONRenderer

import pandas as pd  # pip install pandas openpyxl
from wordcloud import WordCloud  # pip install wordcloud


class PandasXlsxRenderer(BaseRenderer):
    media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    format = "xlsx"
    render_style = "binary"

    def render(self, data, accepted_media_type=None, renderer_context=None) -> BytesIO:
        io = BytesIO()
        df = pd.DataFrame(data)
        df.to_excel(io)  # noqa
        io.seek(0)
        return io


# https://github.com/amueller/word_cloud
class WordcloudRenderer(BaseRenderer):
    media_type = "image/svg+xml"
    format = "svg"
    render_style = "text"

    def render(self, data, accepted_media_type=None, renderer_context=None) -> str:
        wordcloud = WordCloud().generate(str(data))
        return wordcloud.to_svg()
