from django import forms
from django.core.validators import RegexValidator

from core.forms.widgets import PhoneNumberInput


class PhoneNumberField(forms.CharField):
    default_error_messages = {
        "invalid": "휴대폰 번호 포맷으로 입력해주세요.",
    }
    widget = PhoneNumberInput
    default_validators = [
        RegexValidator(r"^01\d[ -]?\d{4}[ -]?\d{4}$"),
    ]

    def __init__(self, *, max_length=13, min_length=11, **kwargs):
        super().__init__(max_length=max_length, min_length=min_length, **kwargs)
