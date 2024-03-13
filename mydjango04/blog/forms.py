from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.bootstrap import PrependedText, TabHolder, Tab
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Field
from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models

from core.crispy_bootstrap5_ext.layout import BorderedTabHolder
from core.forms.widgets import HorizontalRadioSelect, StarRatingSelect
from .models import Review, Memo, Tag


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["message", "rating"]
        widgets = {
            "rating": StarRatingSelect(
                choices=[(i, i) for i in range(1, 6)],
            ),
        }


class DemoForm(forms.Form):
    author = forms.CharField(label="작성자")
    instagram_username = forms.CharField(label="인스타그램 아이디")
    title = forms.CharField(label="제목")
    summary = forms.CharField(
        label="요약",
        help_text="본문에 대한 요약을 최소 20자, 최대 200자 내로 입력해주세요.",
        validators=[MinLengthValidator(20), MaxLengthValidator(200)],
    )
    content = forms.CharField(widget=forms.Textarea, label="내용")
    content_en = forms.CharField(widget=forms.Textarea, label="내용(영문)")

    field_order = [
        "title",
        "summary",
        "author",
        "instagram_username",
    ]  # 필드 순서 배치를 지원

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_action = ""
        # self.helper.form_tag = True
        # self.helper.disable_csrf = False
        # self.helper.form_class = "form-horizontal"
        # self.helper.label_class = "col-sm-4"
        # self.helper.field_class = "col-sm-8"
        self.helper.attrs = {"novalidate": True}
        self.helper.layout = Layout(
            FloatingField("title"),
            "summary",
            BorderedTabHolder(
                Tab("내용", "content"),
                Tab("내용 (영문)", "content_en"),
            ),
            Row(
                Field("author", autocomplete="off", wrapper_class="col-sm-6"),
                PrependedText("instagram_username", "@", wrapper_class="col-sm-6"),
            ),
        )
        self.helper.add_input(Submit("submit", "제출"))

    def clean(self):
        content = self.cleaned_data.get("content")
        summary = self.cleaned_data.get("summary")

        if content and not summary:
            raise forms.ValidationError("본문에 대한 요약을 입력해주세요.")


class MemoForm(forms.ModelForm):
    class Meta:
        model = Memo
        fields = ["message", "status"]


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name"]
