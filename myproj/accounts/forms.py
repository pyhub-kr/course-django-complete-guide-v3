import os

from PIL import Image
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.core.files import File
from django.core.files.base import ContentFile
from django.forms import ModelForm

from accounts.models import User, Profile


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("email",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email:
            user_qs = User.objects.filter(email__iexact=email)
            if user_qs.exists():
                raise ValidationError("이미 등록된 이메일 주소입니다.")
        return email

    helper = FormHelper()
    helper.attrs = {"novalidate": True}
    helper.layout = Layout("username", "email", "password1", "password2")
    helper.add_input(Submit("submit", "회원가입", css_class="w-100"))


class LoginForm(AuthenticationForm):
    helper = FormHelper()
    helper.attrs = {"novalidate": True}
    helper.layout = Layout("username", "password")
    helper.add_input(Submit("submit", "로그인", css_class="w-100"))


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar", "bio", "url"]

    helper = FormHelper()
    helper.attrs = {"novalidate": True}
    helper.layout = Layout("avatar", "bio", "url")
    helper.add_input(Submit("submit", "저장", css_class="w-100"))

    def clean_avatar(self):
        avatar_file: File = self.cleaned_data.get("avatar")
        if avatar_file:
            img = Image.open(avatar_file)
            MAX_SIZE = (512, 512)
            img.thumbnail(MAX_SIZE)
            img = img.convert("RGB")

            thumb_name = os.path.splitext(avatar_file.name)[0] + ".jpg"
            thumb_file = ContentFile(b"", name=thumb_name)
            img.save(thumb_file, format="jpeg")

            return thumb_file

        return avatar_file
