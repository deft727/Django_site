from django import forms
from .models import ContactQuestions


class ContactForms(forms.ModelForm):
    class Meta:
        model = ContactQuestions
        fields = '__all__'