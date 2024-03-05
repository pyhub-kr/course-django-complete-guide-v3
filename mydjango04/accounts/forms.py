import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password

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

    is_profile_update = forms.BooleanField(
        required=False,  # 체크하지 않아도 유효성 검사에 통과하기
        initial=True,
        label="프로필 수정 여부",
        help_text="체크 해제하시면 프로필 수정 단계를 생략합니다.",
    )


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


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, strip=False)
    new_password1 = forms.CharField(widget=forms.PasswordInput, strip=False)
    new_password2 = forms.CharField(widget=forms.PasswordInput, strip=False)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_old_password(self) -> str:
        old_password = self.cleaned_data.get("old_password")
        # 유저의 기존 암호와 같은 지 비교 !!!
        if self.user.check_password(old_password) is False:
            raise forms.ValidationError("기존 암호와 일치하지 않습니다.")
        return old_password

    def clean_new_password2(self) -> str:
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("새로운 두 암호가 일치하지 않습니다.")

        validate_password(password2, self.user)

        return password2

    def save(self, commit=True) -> User:
        password = self.cleaned_data.get("new_password1")
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user
