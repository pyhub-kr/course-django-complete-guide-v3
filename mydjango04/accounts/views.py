from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import default_storage
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


class UserProfileWizardView(LoginRequiredMixin, SessionWizardView):
    form_list = [
        ("profile_form", UserProfileForm),
        ("user_form", UserForm),
    ]
    template_name = "accounts/profile_wizard.html"
    file_storage = default_storage

    def get_form_instance(self, step):
        if step == "profile_form":
            profile, __ = Profile.objects.get_or_create(user=self.request.user)
            return profile
        elif step == "user_form":
            return self.request.user

        return super().get_form_instance(step)

    def done(self, form_list, form_dict, **kwargs):  # noqa
        for form in form_list:
            form.save()
        messages.success(self.request, "프로필을 저장했습니다.")
        return redirect("accounts:profile_wizard")


profile_wizard = UserProfileWizardView.as_view()
