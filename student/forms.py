from django import forms
from django.forms import TextInput, EmailInput, NumberInput, Select, Textarea, DateInput

from student.models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'  # specificam fieldurile dorite in interfata paginii unde este formularul

        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter a first name'}),
            'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter a last name'}),
            'email': EmailInput(attrs={'class': 'form-control', 'placeholder': 'Please enter an email'}),
            'age': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Please enter an age'}),
            'gender': Select(attrs={'class': 'form-select'}),
            'description': Textarea(attrs={'class': 'form-control', 'placeholder': 'Please enter a description', 'rows': 3}),
            'start_date': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'trainer': Select(attrs={'class': 'form-select'})
        }

    # def clean() -> este folosita pentru a verifica corectitudinea datelor introduse in formular in caz contrar,
    # sa genereze o eroare.

    def clean(self):
        cleaned_data = self.cleaned_data

        # O unicitate pe adresa de email
        get_email = cleaned_data.get('email')
        check_email = Student.objects.filter(email=get_email)
        if check_email:
            msg = 'Email-ul exista deja'
            self.add_error('email', msg)

        # O validare pentru unicitate first_name si last_name. Nu vrem sa avem salvati doi studenti cu acelasi first_name SI last_name
        get_first_name = cleaned_data.get('first_name')
        get_last_name = cleaned_data.get('last_name')
        check_name = Student.objects.filter(first_name=get_first_name, last_name=get_last_name)
        if check_name:
            msg = 'Already exist'
            self.add_error('first_name', msg)
            self.add_error('last_name', msg)

        # O validare in care NU salvez un student care are start_date > end_date
        check_start_date = cleaned_data.get('start_date')
        check_end_date = cleaned_data.get('end_date')
        if check_start_date > check_end_date:
            msg = 'Start date must be less than end date'
            self.add_error('start_date', msg)

        # O validare in care utilizatorul este obligat sa scrie minim 10 caractere in campul description
        check_description = cleaned_data.get('description')
        if len(check_description) < 10:
            msg = 'Description must be at least 10 characters'
            self.add_error('description', msg)

        return cleaned_data


class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        # fields = '__all__'
        fields = '__all__'  # specificam fieldurile dorite in interfata paginii unde este formularul

        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter a first name'}),
            'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter a last name'}),
            'email': EmailInput(attrs={'class': 'form-control', 'placeholder': 'Please enter an email'}),
            'age': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Please enter an age'}),
            'gender': Select(attrs={'class': 'form-select'}),
            'description': Textarea(attrs={'class': 'form-control', 'placeholder': 'Please enter a description', 'rows': 3}),
            'start_date': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'trainer': Select(attrs={'class': 'form-select'})
        }
