from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from photolog.forms import NoteForm
from photolog.models import Note, Photo


def index(request):
    note_qs = Note.objects.all().select_related("author").prefetch_related("photo_set")
    return render(
        request,
        "photolog/index.html",
        {
            "note_list": note_qs,
        },
    )


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    form_class = NoteForm
    template_name = "crispy_form.html"
    extra_context = {"form_title": "새 기록"}

    def form_valid(self, form):
        self.object = form.save(commit=False)  # noqa

        new_note = self.object
        new_note.author = self.request.user
        new_note.save()

        photo_file_list = form.cleaned_data.get("photos")
        if photo_file_list:
            Photo.create_photos(new_note, photo_file_list)

        messages.success(self.request, "새 기록을 저장했습니다.")

        return redirect(self.get_success_url())


note_new = NoteCreateView.as_view()


@login_required
def note_edit(request, pk):
    note = get_object_or_404(Note, pk=pk, author=request.user)

    if request.method == "GET":
        form = NoteForm(instance=note)
    else:
        form = NoteForm(data=request.POST, files=request.FILES, instance=note)
        if form.is_valid():
            saved_note = form.save()

            photo_file_list = form.cleaned_data.get("photos")
            if photo_file_list:
                Photo.create_photos(saved_note, photo_file_list)

            messages.success(request, f"기록#{saved_note.pk}을 수정했습니다.")

            return redirect(saved_note)

    return render(
        request,
        "crispy_form.html",
        {
            "form_title": "기록 수정",
            "form": form,
        },
    )


class NoteDetailView(DetailView):
    model = Note


note_detail = NoteDetailView.as_view()
