# core/forms/widgets.py
import re
from typing import Tuple

from django.forms import (
    TextInput,
    CheckboxInput,
    ClearableFileInput,
    RadioSelect,
    Select,
    MultiWidget,
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
