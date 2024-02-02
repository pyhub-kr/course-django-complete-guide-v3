# core/forms/widgets.py

from django.forms import TextInput


class CounterTextInput(TextInput):
    template_name = "core/forms/widgets/counter_text.html"
