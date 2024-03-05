from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView as DjangoPasswordChangeView
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from formtools.wizard.views import SessionWizardView
from vanilla import UpdateView, CreateView

from accounts.forms import (
    ProfileForm,
    UserForm,
    UserProfileForm,
    SignupForm,
    ProfileUserForm,
    # PasswordChangeForm,
)
from accounts.models import Profile


@login_required
def profile_edit(request):
    try:
        instance = request.user.profile
    except Profile.DoesNotExist:
        instance = None

    if request.method == "GET":
        profile_user_form = ProfileUserForm(
            prefix="profile-user", instance=request.user
        )
        profile_form = ProfileForm(prefix="profile", instance=instance)
    else:
        profile_user_form = ProfileUserForm(
            prefix="profile-user",
            data=request.POST,
            files=request.FILES,
            instance=request.user,
        )
        profile_form = ProfileForm(
            prefix="profile", data=request.POST, files=request.FILES, instance=instance
        )
        if profile_user_form.is_valid() and profile_form.is_valid():
            profile_user_form.save()

            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect("accounts:profile_edit")

    return render(
        request,
        "accounts/profile_form.html",
        {
            "profile_user_form": profile_user_form,
            "profile_form": profile_form,
        },
    )


# class ProfileUpdateView(LoginRequiredMixin, UpdateView):
#     model = Profile
#     form_class = ProfileForm
#     success_url = reverse_lazy("accounts:profile_edit")
#
#     def get_object(self):
#         try:
#             return self.request.user.profile
#         except Profile.DoesNotExist:
#             return None
#
#     def form_valid(self, form):
#         profile = form.save(commit=False)
#         profile.user = self.request.user
#         return super().form_valid(form)
#
#
# profile_edit = ProfileUpdateView.as_view()


def check_is_profile_update(wizard_view: "UserProfileWizardView") -> bool:
    cleaned_data = wizard_view.get_cleaned_data_for_step("user_form")
    if cleaned_data is None:
        return True
    return cleaned_data.get("is_profile_update", False)


class UserProfileWizardView(LoginRequiredMixin, SessionWizardView):
    form_list = [
        ("user_form", UserForm),
        ("profile_form", UserProfileForm),
    ]
    template_name = "accounts/profile_wizard.html"
    file_storage = default_storage

    condition_dict = {
        "profile_form": check_is_profile_update,
    }

    def get_form_instance(self, step):
        if step == "profile_form":
            profile, __ = Profile.objects.get_or_create(user=self.request.user)
            return profile
        elif step == "user_form":
            return self.request.user

        return super().get_form_instance(step)

    def done(self, form_list, form_dict, **kwargs):  # noqa
        # print("form_list :", form_list)
        # print("form_dict :", form_dict)
        # for form in form_list:
        #     form.save()

        # form_list[0].save()
        # form_list[1].save()

        user = form_dict["user_form"].save()

        if "profile_form" in form_dict:
            profile = form_dict["profile_form"].save(commit=False)
            profile.user = user
            profile.save()

        messages.success(self.request, "프로필을 저장했습니다.")
        return redirect("accounts:profile_wizard")


profile_wizard = UserProfileWizardView.as_view()


# def login(request):
#     if request.method == "GET":
#         return render(request, "accounts/login_form.html")
#     else:
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#
#         user = authenticate(request, username=username, password=password)
#         if user is None:
#             return HttpResponse("인증 실패", status=400)
#
#         if user.is_active is False:
#             return HttpResponse("비활성화된 계정입니다.", status=400)
#
#         request.session["_auth_user_backend"] = user.backend
#         request.session["_auth_user_id"] = user.pk
#         request.session["_auth_user_hash"] = user.get_session_auth_hash()
#
#         next_url = (
#             request.POST.get("next")
#             or request.GET.get("next")
#             or settings.LOGIN_REDIRECT_URL
#         )
#         return redirect(next_url)


class LoginView(DjangoLoginView):
    template_name = "accounts/login_form.html"
    # redirect_authenticated_user = True
    # next_page = "accounts:profile"


login = LoginView.as_view()


def profile(request):
    return HttpResponse(
        f"username : {request.user.username}, {request.user.is_authenticated}"
    )


# def signup(request):
#     if request.method == "GET":
#         form = SignupForm()
#     else:
#         form = SignupForm(data=request.POST, files=request.FILES)
#         if form.is_valid():
#             created_user = form.save()
#             auth_login(request, created_user)
#
#             next_url = request.POST.get("next") or request.GET.get("next")
#             url_is_safe = url_has_allowed_host_and_scheme(
#                 url=next_url,
#                 allowed_hosts={request.get_host()},
#                 require_https=request.is_secure(),
#             )
#             if url_is_safe is False:
#                 next_url = ""
#
#             # return redirect(settings.LOGIN_URL)  # "/accounts/login/"
#             return redirect(next_url or settings.LOGIN_REDIRECT_URL)
#
#     return render(
#         request,
#         "accounts/signup_form.html",
#         {
#             "form": form,
#         },
#     )


class SignupView(CreateView):
    form_class = SignupForm
    template_name = "accounts/signup_form.html"
    success_url = settings.LOGIN_REDIRECT_URL

    def form_valid(self, form) -> HttpResponse:
        response = super().form_valid(form)
        created_user = form.instance
        auth_login(self.request, created_user)
        return response

    def get_success_url(self) -> str:
        next_url = self.request.POST.get("next") or self.request.GET.get("next")
        if next_url:
            url_is_safe = url_has_allowed_host_and_scheme(
                url=next_url,
                allowed_hosts={self.request.get_host()},
                require_https=self.request.is_secure(),
            )
            if url_is_safe:
                return next_url
        return super().get_success_url()


signup = SignupView.as_view()


# @csrf_protect
# @never_cache
# @require_POST  # auth.LogoutView에서는 장고 5.0부터 GET 요청을 통한 로그아웃을 지원하지 않습니다.
# def logout(request):
#     auth_logout(request)
#
#     next_url = request.POST.get("next")
#     if next_url:
#         url_is_safe = url_has_allowed_host_and_scheme(
#             url=next_url,
#             allowed_hosts={request.get_host()},
#             require_https=request.is_secure(),
#         )
#         if url_is_safe:
#             return redirect(next_url)
#
#     return redirect(settings.LOGIN_URL)
#
#     # return render(request, "registration/logged_out.html")


logout = LogoutView.as_view(
    # 템플릿 파일을 변경하시거나,
    # template_name="registration/logged_out.html",
    # next_page 인자를 지정하면, 최소한 템플릿 응답은 없습니다.
    next_page=settings.LOGIN_URL,
)


# @login_required
# def password_change(request):
#     if request.method == "GET":
#         form = PasswordChangeForm(request.user)
#     else:
#         form = PasswordChangeForm(request.user, data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             update_session_auth_hash(request, request.user)
#             messages.success(request, "암호를 변경했습니다.")
#             return redirect("accounts:profile")
#
#     return render(
#         request,
#         "accounts/password_change_form.html",
#         {
#             "form": form,
#         },
#     )


class PasswordChangeView(DjangoPasswordChangeView):
    success_url = reverse_lazy("accounts:profile")
    template_name = "accounts/password_change_form.html"


password_change = PasswordChangeView.as_view()
