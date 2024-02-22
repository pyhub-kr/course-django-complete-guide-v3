import datetime

from django import forms

# from core.forms.fields import PhoneNumberField, DatePickerField
from core.forms.widgets import (
    PhoneNumberInput,
    DatePickerInput,
    DatePickerOptions,
    NaverMapPointInput,
)
from .models import Profile, User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["address", "phone_number", "photo"]


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
            "location_point",
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
            "location_point": NaverMapPointInput,
            "phone_number": PhoneNumberInput,
        }
