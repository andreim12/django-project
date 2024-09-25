import django_filters
from django import forms

from student.models import Student
from trainer.models import Trainer


# Lookup expr: exact, icontains, startswith, endswith, lte, lt, gte, gt

# exact -> trebuie sa fie 1to1 cu cea salvata in tabela. TINE CONT DE CASE-SENSITIVE
# icontains -> daca stringul introdus este inclus intr-un alt string
# startswith -> daca stringul introdus este la inceputul unui alt string
# endswith -> daca stringul introdus este la sfarstiul unui alt string


# lte - less than or equal to
# lt - less than
# gte - greater than or equal to
# gt - greater than


class StudentFilters(django_filters.FilterSet):

    first_name = django_filters.CharFilter(lookup_expr='icontains', label='First name', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter a first name'}))
    last_name = django_filters.CharFilter(lookup_expr='icontains', label='Last name', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter a last name'}))
    age = django_filters.CharFilter(lookup_expr='icontains', label='Age', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Please enter an age'}))
    # email = django_filters.CharFilter(lookup_expr='icontains', label='Email', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter an email'}))
    list_emails = list(set([(student.email, student.email) for student in Student.objects.filter(active=True)]))
    email = django_filters.ChoiceFilter(choices=list_emails, widget=forms.Select(attrs={'class': 'form-control'}))

    start_date_gte = django_filters.DateFilter(field_name='start_date', lookup_expr='gte', label='From start date', widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    start_date_lte = django_filters.DateFilter(field_name='start_date', lookup_expr='lte', label='To start date', widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    list_trainers_active = [(trainer.id, trainer) for trainer in Trainer.objects.filter(active=True)]
    # trainer = django_filters.ChoiceFilter(choices=list_trainers_active, widget=forms.Select(attrs={'class': 'form-select'}))
    trainer = django_filters.ChoiceFilter(choices=list_trainers_active, widget=forms.RadioSelect)

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'age', 'email', 'start_date_gte', 'start_date_lte', 'trainer']
