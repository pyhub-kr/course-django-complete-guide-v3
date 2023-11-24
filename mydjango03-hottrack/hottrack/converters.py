# hottrack/converters.py

from datetime import date
from django.urls import register_converter


class DateConverter:
    # year: 2000 ~ 2099
    # month: 1, 2, 3, 4, 5, 6, 7, 8, 9, 01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12
    # day : 1, 2, 3, .. 9, 01, 02, 03, .. 09, 10, 11, 12, .. 30, 31
    regex = r"20\d{2}/([1-9]|0[1-9]|1[0-2]){1,2}/([1-9]|0[1-9]|[12][0-9]|3[01]){1,2}"
    # regex = r"\d{4}/\d{1,2}/\d{1,2}"

    def to_python(self, value: str) -> date:
        year, month, day = map(int, value.split("/"))
        return date(year, month, day)

    def to_url(self, value: date) -> str:
        return f"{value.year}/{value.month:02d}/{value.day:02d}"


# Django에 DateConverter 등록
register_converter(DateConverter, "date")
