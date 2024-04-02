from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django_htmx.http import trigger_client_event

from core.decorators import login_required_hx
from photolog.forms import (
    NoteCreateForm,
    PhotoUpdateFormSet,
    NoteUpdateForm,
    CommentForm,
)
from photolog.models import Note, Photo, Comment


def index(request):
    note_qs = Note.objects.all()

    tag_name = request.GET.get("tag", "").strip()
    if tag_name:
        note_qs = note_qs.filter(tags__name__in=[tag_name])

    note_qs = note_qs.select_related("author").prefetch_related("photo_set", "tags")

    return render(
        request,
        "photolog/index.html",
        {
            "note_list": note_qs,
        },
    )


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    form_class = NoteCreateForm
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
    photo_qs = note.photo_set.all()

    if request.method == "GET":
        note_form = NoteUpdateForm(instance=note, prefix="note")
        photo_formset = PhotoUpdateFormSet(
            queryset=photo_qs,
            instance=note,
            prefix="photos",
        )
    else:
        note_form = NoteUpdateForm(
            data=request.POST, files=request.FILES, instance=note, prefix="note"
        )
        photo_formset = PhotoUpdateFormSet(
            queryset=photo_qs,
            instance=note,
            data=request.POST,
            files=request.FILES,
            prefix="photos",
        )

        if note_form.is_valid() and photo_formset.is_valid():
            saved_note = note_form.save()

            # 새롭게 생성되는 Photo
            photo_file_list = note_form.cleaned_data.get("photos")
            if photo_file_list:
                Photo.create_photos(saved_note, photo_file_list)

            # 기존 Photo 수정
            photo_formset.save()

            messages.success(request, f"기록#{saved_note.pk}을 수정했습니다.")

            return redirect(saved_note)

    return render(
        request,
        "crispy_form_and_formset.html",
        {
            "form_title": "기록 수정",
            "form": note_form,
            "formset": photo_formset,
            "form_submit_label": "저장하기",
        },
    )


class NoteDetailView(DetailView):
    model = Note


note_detail = NoteDetailView.as_view()


class CommentListView(ListView):
    model = Comment
    template_name = "photolog/_comment_list.html"


comment_list = CommentListView.as_view()


@method_decorator(login_required_hx, name="dispatch")
class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "photolog/_comment_form.html"

    def dispatch(self, request, *args, **kwargs):
        note_pk = self.kwargs["note_pk"]
        self.note = get_object_or_404(Note, pk=note_pk)  # noqa
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):  # 유효성 검사가 끝나고 나서 호출
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.note = self.note
        comment.save()

        messages.success(self.request, "태그를 저장했습니다.")

        response = render(self.request, "_messages_as_event.html")
        response = trigger_client_event(response, "refresh-comment-list")

        return response


comment_new = CommentCreateView.as_view()
