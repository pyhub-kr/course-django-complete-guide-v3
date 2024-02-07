from django import forms

from core.forms.fields import PhoneNumberField
from core.forms.widgets import PhoneNumberInput
from .models import Profile


class ProfileForm(forms.ModelForm):
    # phone_number = PhoneNumberField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["address"].required = True

    class Meta:
        model = Profile
        fields = [
            "address",
            "phone_number",
            "photo",
        ]
        widgets = {
            "phone_number": PhoneNumberInput,
        }
