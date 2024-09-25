import django_filters
from django import forms

from trainer.models import Trainer


class TrainerFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains', label='First name', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Please enter a first name'}))
    last_name = django_filters.CharFilter(lookup_expr='icontains', label='Last name', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Please enter a last name'}))
    course = django_filters.CharFilter(lookup_expr='icontains', label='Course', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Please enter a course'}))
    email = django_filters.CharFilter(lookup_expr='icontains', label='Email', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Please enter an email'}))


class Meta:
    model = Trainer
    fields = ['first_name', 'last_name', 'course', 'email']
