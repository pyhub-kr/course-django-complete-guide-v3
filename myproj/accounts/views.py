from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.shortcuts import render

from accounts.forms import LoginForm


class LoginView(DjangoLoginView):
    form_class = LoginForm
    template_name = "crispy_form.html"
    extra_context = {
        "form_title": "로그인",
    }


login = LoginView.as_view()


@login_required
def profile(request):
    return render(request, "accounts/profile.html")
