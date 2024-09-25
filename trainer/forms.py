from django import forms
from django.forms import TextInput, EmailInput

from trainer.models import Trainer


class TrainerForm(forms.ModelForm):
    class Meta:
        model = Trainer
        fields = '__all__'

        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter a first name'}),
            'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter a last name'}),
            'course': TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter a course'}),
            'email': EmailInput(attrs={'class': 'form-control', 'placeholder': 'Please enter an email'})
        }


class TrainerUpdateForm(forms.ModelForm):
    class Meta:
        model = Trainer
        fields = '__all__'

        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter a first name'}),
            'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter a last name'}),
            'course': TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter a course'}),
            'email': EmailInput(attrs={'class': 'form-control', 'placeholder': 'Please enter an email'})
        }
