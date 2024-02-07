from django import forms

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
