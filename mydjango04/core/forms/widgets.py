# core/forms/widgets.py

from django.forms import (
    TextInput,
    CheckboxInput,
    ClearableFileInput,
    RadioSelect,
    Select,
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
