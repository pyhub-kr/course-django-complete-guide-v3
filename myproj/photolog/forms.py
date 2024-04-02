from typing import List

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms
from django.core.files import File

from .models import Note, Photo


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleImageField(forms.ImageField):
    widget = MultipleFileInput

    def clean(self, data, initial=None):
        single_clean = super().clean  # 함수를 호출하지 않습니다.
        if isinstance(data, (list, tuple)):
            return [single_clean(file) for file in data]
        else:
            return single_clean(data)


class NoteForm(forms.ModelForm):
    photos = MultipleImageField()

    class Meta:
        model = Note
        fields = ["title", "content"]

    helper = FormHelper()
    helper.attrs = {"novalidate": True}
    helper.layout = Layout("title", "content", "photos")
    helper.add_input(Submit("submit", "저장하기", css_class="w-100"))

    def clean_photos(self):
        file_list: List[File] = self.cleaned_data.get("photos")
        if not file_list:
            raise forms.ValidationError("최소 1개의 사진을 등록해주세요.")
        elif file_list:
            try:
                file_list = [Photo.make_thumb(file) for file in file_list]
            except Exception as e:
                raise forms.ValidationError(
                    "썸네일 생성 중에 오류가 발생했습니다."
                ) from e
        return file_list
