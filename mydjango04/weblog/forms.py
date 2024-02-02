from django import forms

from core.forms.widgets import CounterTextInput
from weblog.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "status",
            "photo",
            "tag_set",
        ]
        widgets = {
            "title": CounterTextInput,
        }


class ConfirmDeleteForm(forms.Form):
    confirm = forms.BooleanField(
        label="동의",
        help_text="삭제에 동의하시면 체크해주세요.",
        required=True,
        error_messages={
            "required": "동의하지 않으시면 삭제할 수 없습니다.",
        },
    )
