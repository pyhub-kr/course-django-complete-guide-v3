# core/forms/widgets.py
import dataclasses
import datetime
import re
from typing import Tuple, List, Callable, Union, Dict

from django.forms import (
    TextInput,
    CheckboxInput,
    ClearableFileInput,
    RadioSelect,
    Select,
    MultiWidget,
    DateInput,
)


class CounterTextInput(TextInput):
    template_name = "core/forms/widgets/counter_text.html"


class IosSwitchInput(CheckboxInput):
    def __init__(self, attrs=None, check_test=None):
        attrs = attrs or {}
        attrs["class"] = attrs.get("class", "") + " ios-form-switch"
        super().__init__(attrs, check_test)

    # Meta로 지정하지마세요.
    class Media:
        css = {
            "all": [
                "core/forms/widgets/ios_form_switch.css",
            ],
        }


class PreviewClearableFileInput(ClearableFileInput):
    template_name = "core/forms/widgets/preview_clearable_file.html"


class HorizontalRadioSelect(RadioSelect):
    template_name = "core/forms/widgets/horizontal_radio.html"


class StarRatingSelect(Select):
    template_name = "core/forms/widgets/star_rating_select.html"

    class Media:
        css = {
            "all": ["core/star-rating-js/4.3.0/star-rating.min.css"],
        }
        js = [
            "core/star-rating-js/4.3.0/star-rating.min.js",
        ]


class PhoneNumberInput(MultiWidget):
    subwidget_default_attrs = {
        "style": "width: 6ch; margin-right: 1ch;",
        "autocomplete": "off",
    }

    def __init__(self, attrs=None):
        widgets = [
            TextInput(
                attrs={
                    **self.subwidget_default_attrs,
                    "pattern": r"01\d",
                    "maxlength": 3,
                },
            ),
            TextInput(
                attrs={
                    **self.subwidget_default_attrs,
                    "pattern": r"\d{4}",
                    "maxlength": 4,
                },
            ),
            TextInput(
                attrs={
                    **self.subwidget_default_attrs,
                    "pattern": r"\d{4}",
                    "maxlength": 4,
                },
            ),
        ]
        super().__init__(widgets, attrs)

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)
        if "maxlength" in attrs:
            del attrs["maxlength"]
        return attrs

    def decompress(self, value: str) -> Tuple[str, str, str]:
        if value:
            value = re.sub(r"[ -]", "", value)
            return value[:3], value[3:7], value[7:]
        return "", "", ""

    def value_from_datadict(self, data, files, name) -> str:
        values = super().value_from_datadict(data, files, name)
        return "".join((value or "") for value in values)


@dataclasses.dataclass
class DatePickerOptions:
    datesDisabled: Union[
        List[datetime.date],
        Callable[[], List[datetime.date]],
    ] = dataclasses.field(default_factory=list)
    format: str = "yyyy-mm-dd"  # 날짜 포맷
    minDate: Union[
        str, int, datetime.date, Callable[[], Union[str, int, datetime.date]]
    ] = None
    maxDate: Union[
        str, int, datetime.date, Callable[[], Union[str, int, datetime.date]]
    ] = None
    todayButton: bool = False
    todayHighlight: bool = False

    def to_dict(self) -> Dict[str, Union[str, int, List[int], List[datetime.date]]]:
        result = {}
        for field in dataclasses.fields(self):
            value = getattr(self, field.name)
            if callable(value):  # value가 함수라면
                value = value()  # 인자없이 호출하여 반환값을 value로서 활용합니다.
            result[field.name] = value
        return result


class DatePickerInput(DateInput):
    template_name = "core/forms/widgets/date_picker.html"

    def __init__(
        self,
        attrs=None,
        format=None,
        date_picker_options: DatePickerOptions = None,
    ):
        self.date_picker_options = date_picker_options or DatePickerOptions()
        super().__init__(attrs, format)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["date_picker_options"] = self.date_picker_options.to_dict()
        return context

    class Media:
        css = {
            "all": [
                "https://cdn.jsdelivr.net/npm/vanillajs-datepicker@1.3.4/dist/css/datepicker-bs5.min.css",
            ],
        }
        js = [
            "https://cdn.jsdelivr.net/npm/vanillajs-datepicker@1.3.4/dist/js/datepicker.min.js",
        ]
