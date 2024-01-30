from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from vanilla import UpdateView

from accounts.forms import ProfileForm
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
