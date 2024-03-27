from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    helper = FormHelper()
    helper.attrs = {"novalidate": True}
    helper.layout = Layout("username", "password")
    helper.add_input(Submit("submit", "로그인", css_class="w-100"))
