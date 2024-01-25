from django import forms


class PostForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)
    status = forms.ChoiceField(
        choices=[
            ("D", "초안"),
            ("P", "발행"),
        ],
    )
    photo = forms.ImageField(required=False)
