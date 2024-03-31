from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, DetailView

from studio.forms import (
    NoteCreateForm,
    PhotoUpdateFormSet,
    NoteUpdateForm,
)
from studio.models import Note, Photo


def index(request):
    note_qs = Note.objects.all().select_related("author").prefetch_related("photo_set")
    return render(
        request,
        "studio/index.html",
        {
            "note_list": note_qs,
        },
    )


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    form_class = NoteCreateForm
    template_name = "crispy_form.html"
    extra_context = {"form_title": "기록 남기기"}

    def form_valid(self, form):
        # get_success_url 내의 format 문자열 조합을 위해 필요
        self.object = form.save(commit=False)

        note = self.object
        note.author = self.request.user
        note.save()

        photo_file_list = form.cleaned_data.get("photos")
        if photo_file_list:
            Photo.create_photos(note, photo_file_list)

        messages.success(self.request, "새로운 노트를 저장했습니다.")

        return redirect(note)


note_new = NoteCreateView.as_view()


@login_required
def note_edit(request, pk):
    note = get_object_or_404(Note, pk=pk)

    photo_qs = Photo.objects.filter(note=note)
    if request.method == "GET":
        note_form = NoteUpdateForm(instance=note, prefix="note")
        photo_formset = PhotoUpdateFormSet(
            queryset=photo_qs,
            instance=note,
            prefix="photos",
        )
    else:
        note_form = NoteUpdateForm(
            data=request.POST,
            files=request.FILES,
            instance=note,
            prefix="note",
        )
        photo_formset = PhotoUpdateFormSet(
            data=request.POST,
            files=request.FILES,
            queryset=photo_qs,
            instance=note,
            prefix="photos",
        )
        if note_form.is_valid() and photo_formset.is_valid():
            note_form.save()

            photo_file_list = note_form.cleaned_data.get("photos")
            if photo_file_list:
                Photo.create_photos(note, photo_file_list)

            photo_formset.save()

            messages.success(request, f"노트#{pk}을(를) 수정했습니다.")
            return redirect(note)

    return render(
        request,
        "crispy_form_and_formset.html",
        {
            "form_title": "노트 수정",
            "form_submit_label": "저장하기",
            "form": note_form,
            "formset": photo_formset,
        },
    )


class NoteDetailView(DetailView):
    model = Note


note_detail = NoteDetailView.as_view()
