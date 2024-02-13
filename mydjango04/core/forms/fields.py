import datetime

from django import forms
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator

from core.forms.widgets import PhoneNumberInput, DatePickerInput


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


class DatePickerField(forms.DateField):
    default_error_messages = {
        "min_value": "%(limit_value)s 이상의 날짜를 선택해주세요.",
        "max_value": "%(limit_value)s 이하의 날짜를 선택해주세요.",
        **forms.DateField.default_error_messages,
    }
    widget = DatePickerInput

    def __init__(self, *, min_value=None, max_value=None, **kwargs):
        self.min_value: datetime.date = min_value
        self.max_value: datetime.date = max_value
        super().__init__(**kwargs)

        if self.min_value is not None:
            self.validators.append(MinValueValidator(self.min_value))

        if self.max_value is not None:
            self.validators.append(MaxValueValidator(self.max_value))

        if isinstance(self.widget, DatePickerInput):
            if (
                self.min_value is not None
                and self.widget.date_picker_options.minDate is None
            ):
                self.widget.date_picker_options.minDate = self.min_value

            if (
                self.max_value is not None
                and self.widget.date_picker_options.maxDate is None
            ):
                self.widget.date_picker_options.maxDate = self.max_value
