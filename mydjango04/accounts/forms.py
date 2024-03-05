import datetime
from typing import Iterator

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpRequest
from django.shortcuts import resolve_url
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

# from core.forms.fields import PhoneNumberField, DatePickerField
from core.forms.widgets import (
    PhoneNumberInput,
    DatePickerInput,
    DatePickerOptions,
    NaverMapPointInput,
)
from .models import Profile, User


token_generator = default_token_generator


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


class ProfileUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email"]

    def clean_email(self) -> str:
        email = self.cleaned_data.get("email")
        if email:
            qs = self._meta.model.objects.filter(email__iexact=email)
            qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("이미 등록된 이메일입니다.")
        return email


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


class PasswordResetForm(forms.Form):
    # 이메일 포맷에 대한 유효성 검사만 수행할 뿐, 이메일의 존재 유무를 확인하지는 않습니다.
    email = forms.EmailField()

    # auth앱의 PasswordResetForm에서는 save 메서드에서 이메일 발송에 필요한
    # 다양한 인자를 전달받습니다.
    def save(self, request: HttpRequest) -> None:
        email = self.cleaned_data.get("email")
        for uidb64, token in self.make_uidb64_and_token(email):
            scheme = "https" if request.is_secure() else "http"
            host = request.get_host()
            # 새로운 암호를 입력받아, 암호를 변경하는 뷰
            path = resolve_url(
                "accounts:password_reset_confirm", uidb64=uidb64, token=token
            )
            reset_url = f"{scheme}://{host}{path}"
            print(
                f"{email} 이메일로 {reset_url} 주소를 발송합니다."
            )  # TODO: 이메일 발송

    def make_uidb64_and_token(self, email: str) -> Iterator[tuple[str, str]]:
        for user in self.get_users(email):
            print(f"{email}에 매칭되는 유저를 찾았습니다.")

            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)

            yield uidb64, token

    def get_users(self, email: str) -> Iterator[User]:
        active_users = User.objects.filter(email__iexact=email, is_active=True)
        return (
            user
            for user in active_users
            if user.has_usable_password() and email == user.email
        )
