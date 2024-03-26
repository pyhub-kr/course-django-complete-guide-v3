from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.forms import LoginForm, SignupForm
from accounts.models import User


class SignupView(CreateView):
    model = User
    form_class = SignupForm
    template_name = "crispy_form.html"
    extra_context = {"form_title": "회원가입"}
    success_url = reverse_lazy("accounts:profile")

    def form_valid(self, form):
        response = super().form_valid(form)
        user: User = self.object
        user.send_welcome_email()
        messages.success(self.request, "회원가입을 환영합니다. ;-)")

        auth_login(self.request, user)
        messages.success(self.request, "자동 로그인했습니다. :D")

        return response


signup = SignupView.as_view()


class LoginView(DjangoLoginView):
    form_class = LoginForm
    template_name = "crispy_form.html"
    extra_context = {"form_title": "로그인"}


login = LoginView.as_view()


@login_required
def profile(request):
    return render(request, "accounts/profile.html")
