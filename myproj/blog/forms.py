# blog/forms.py

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from django import forms
from .models import Todo


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["id", "text", "done"]

    helper = FormHelper()
    helper.attrs = {"novalidate": True}
    helper.layout = Layout("text", "done")
    helper.add_input(Submit("submit", "저장하기", css_class="w-100"))
