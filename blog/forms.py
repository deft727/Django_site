from django import forms
from .models import PostRewiews


class ReviewsForm(forms.ModelForm):

    class Meta:
        model= PostRewiews
        fields= ('text',)