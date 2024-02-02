# core/forms/widgets.py

from django.forms import TextInput, CheckboxInput


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
