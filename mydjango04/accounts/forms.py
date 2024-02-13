import datetime

from django import forms

# from core.forms.fields import PhoneNumberField, DatePickerField
from core.forms.widgets import PhoneNumberInput, DatePickerInput, DatePickerOptions
from .models import Profile


class ProfileForm(forms.ModelForm):
    # mydate = DatePickerField(
    #     min_value=lambda: datetime.date.today(),
    #     max_value=lambda: datetime.date.today() + datetime.timedelta(days=7),
    # )

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
                    todayButton=True,
                    todayHighlight=True,
                ),
            ),
            "phone_number": PhoneNumberInput,
        }
