from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError

from accounts.models import User


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        # TypeError: can only concatenate tuple (not "list") to tuple
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
    helper.layout = Layout(
        "username",
        "email",
        "password1",
        "password2",
    )
    helper.add_input(
        Submit(name="submit", value="회원가입", css_class="w-100"),
    )


class LoginForm(AuthenticationForm):
    helper = FormHelper()
    helper.attrs = {"novalidate": True}
    helper.layout = Layout(
        "username",
        "password",
    )
    helper.add_input(Submit("submit", "로그인", css_class="w-100"))
