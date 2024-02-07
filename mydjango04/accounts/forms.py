import datetime

from django import forms

from core.forms.fields import PhoneNumberField
from core.forms.widgets import PhoneNumberInput, DatePickerInput, DatePickerOptions
from .models import Profile


class ProfileForm(forms.ModelForm):
    # phone_number = PhoneNumberField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["address"].required = True

    class Meta:
        model = Profile
        fields = [
            "birth_date",
            "address",
            "phone_number",
            "photo",
        ]
        widgets = {
            "birth_date": DatePickerInput(
                date_picker_options=DatePickerOptions(
                    datesDisabled=lambda: [
                        datetime.date.today() + datetime.timedelta(days=2),
                    ],
                    minDate=lambda: datetime.date.today(),
                    maxDate=lambda: datetime.date.today() + datetime.timedelta(days=7),
                    todayButton=True,
                    todayHighlight=True,
                ),
            ),
            "phone_number": PhoneNumberInput,
        }
