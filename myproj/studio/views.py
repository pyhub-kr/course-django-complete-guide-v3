from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from studio.forms import NoteForm
from studio.models import Note, Photo


def index(request):
    note_list = range(100)
    return render(
        request,
        "studio/index.html",
        {
            "note_list": note_list,
        },
    )


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    form_class = NoteForm
    template_name = "crispy_form.html"
    extra_context = {"form_title": "기록 남기기"}
    success_url = reverse_lazy("studio:index")

    def form_valid(self, form):
        self.object = form.save(commit=False)

        note = self.object
        note.author = self.request.user
        note.save()

        photo_file_list = form.cleaned_data.get("photos")
        Photo.create_photos(note, photo_file_list)

        messages.success(self.request, "새로운 노트를 저장했습니다.")

        return redirect(self.get_success_url())


note_new = NoteCreateView.as_view()
