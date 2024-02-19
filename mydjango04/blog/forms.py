from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator

from core.forms.widgets import HorizontalRadioSelect, StarRatingSelect
from .models import Review


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

    def clean(self):
        content = self.cleaned_data.get("content")
        summary = self.cleaned_data.get("summary")

        if content and not summary:
            raise forms.ValidationError("본문에 대한 요약을 입력해주세요.")
