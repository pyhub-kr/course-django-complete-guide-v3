from typing import Optional

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as DjangoLoginView, RedirectURLMixin
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from accounts.forms import LoginForm, SignupForm, ProfileForm
from accounts.models import User, Profile
from accounts.utils import send_welcome_email


class SignupView(RedirectURLMixin, CreateView):
    model = User
    form_class = SignupForm
    template_name = "crispy_form.html"
    extra_context = {
        "form_title": "회원가입",
    }
    success_url = reverse_lazy("accounts:profile")

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            redirect_to = self.success_url
            if redirect_to != request.path:
                messages.warning(request, "로그인 유저는 회원가입할 수 없습니다.")
                return HttpResponseRedirect(redirect_to)
        response = super().dispatch(request, *args, **kwargs)
        return response

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "회원가입을 환영합니다. ;-)")

        user = self.object
        auth_login(self.request, user)
        messages.success(self.request, "회원가입과 동시에 로그인 지원 !")

        send_welcome_email(user, fail_silently=True)

        return response


signup = SignupView.as_view()


class LoginView(DjangoLoginView):
    redirect_authenticated_user = True
    form_class = LoginForm
    template_name = "crispy_form.html"
    extra_context = {
        "form_title": "로그인",
    }
    success_url_allowed_hosts: set = settings.SUCCESS_URL_ALLOWED_HOSTS


login = LoginView.as_view()


class LogoutView(DjangoLogoutView):
    next_page = "accounts:login"
    success_url_allowed_hosts: set = settings.SUCCESS_URL_ALLOWED_HOSTS

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.success(request, "로그아웃했습니다. :-)")
        return response


logout = LogoutView.as_view()


@login_required
def profile(request):
    return render(request, "accounts/profile.html")


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "crispy_form.html"
    extra_context = {"form_title": "프로필 수정"}
    success_url = reverse_lazy("accounts:profile")

    def get_object(self, queryset=None) -> Optional[Profile]:
        if not self.request.user.is_authenticated:
            return None

        try:
            return self.request.user.profile
        except Profile.DoesNotExist:
            return None

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "프로필을 저장했습니다.")
        return response


profile_edit = ProfileUpdateView.as_view()
