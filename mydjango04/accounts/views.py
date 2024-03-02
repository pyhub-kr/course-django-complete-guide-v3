from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from formtools.wizard.views import SessionWizardView
from vanilla import UpdateView

from accounts.forms import ProfileForm, UserForm, UserProfileForm
from accounts.models import Profile


# @login_required
# def profile_edit(request):
#     try:
#         instance = request.user.profile
#     except Profile.DoesNotExist:
#         instance = None
#
#     if request.method == "GET":
#         form = ProfileForm(instance=instance)
#     else:
#         form = ProfileForm(data=request.POST, files=request.FILES, instance=instance)
#         if form.is_valid():
#             profile = form.save(commit=False)
#             profile.user = request.user
#             profile.save()
#             return redirect("accounts:profile_edit")
#
#     return render(
#         request,
#         "accounts/profile_form.html",
#         {
#             "form": form,
#         },
#     )


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    success_url = reverse_lazy("accounts:profile_edit")

    def get_object(self):
        try:
            return self.request.user.profile
        except Profile.DoesNotExist:
            return None

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.user = self.request.user
        return super().form_valid(form)


profile_edit = ProfileUpdateView.as_view()


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


def login(request):
    if request.method == "GET":
        return render(request, "accounts/login_form.html")
    else:
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is None:
            return HttpResponse("인증 실패", status=400)

        request.session["_auth_user_backend"] = user.backend
        request.session["_auth_user_id"] = user.pk
        request.session["_auth_user_hash"] = user.get_session_auth_hash()

        next_url = (
            request.POST.get("next")
            or request.GET.get("next")
            or settings.LOGIN_REDIRECT_URL
        )
        return redirect(next_url)


def profile(request):
    return HttpResponse(
        f"username : {request.user.username}, {request.user.is_authenticated}"
    )
