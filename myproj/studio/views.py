from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django_htmx.http import trigger_client_event

from core.decorators import login_required_hx
from studio.forms import (
    NoteCreateForm,
    PhotoUpdateFormSet,
    NoteUpdateForm,
    CommentForm,
)
from studio.models import Note, Photo, Comment


def index(request):
    note_qs = Note.objects.all()

    tag_name = request.GET.get("tag", "").strip()
    if tag_name:
        note_qs = note_qs.filter(tags__name__in=[tag_name])

    note_qs = note_qs.select_related("author").prefetch_related("photo_set", "tags")

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

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        note = self.object
        context_data["comment_list"] = note.comment_set.select_related(
            "author__profile"
        )
        return context_data


note_detail = NoteDetailView.as_view()


class CommentListView(ListView):
    template_name = "studio/_comment_list.html"

    def get_queryset(self) -> QuerySet[Comment]:
        note_pk = self.kwargs["note_pk"]
        return Comment.objects.filter(note__pk=note_pk).select_related(
            "author__profile"
        )


comment_list = CommentListView.as_view()


# 함수 장식자로도 클래스 기반 뷰에 적용 가능


@method_decorator(login_required_hx, name="dispatch")
class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "studio/_comment_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.note = get_object_or_404(Note, pk=kwargs["note_pk"])  # noqa
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.note = self.note
        comment.author = self.request.user
        comment.save()

        messages.success(self.request, "태그를 저장했습니다.")
        response = render(self.request, "_messages_as_event.html")
        response = trigger_client_event(response, "refresh-comment-list")
        return response


comment_new = CommentCreateView.as_view()


@method_decorator(login_required_hx, name="dispatch")
class CommentUpdateView(UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "studio/_comment_form.html"

    def get_queryset(self):
        note_pk = self.kwargs["note_pk"]
        qs = super().get_queryset()
        qs = qs.filter(note__pk=note_pk, author=self.request.user)
        return qs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "태그를 저장했습니다.")
        response = render(self.request, "_messages_as_event.html")
        response = trigger_client_event(response, "refresh-comment-list")
        return response


comment_edit = CommentUpdateView.as_view()
