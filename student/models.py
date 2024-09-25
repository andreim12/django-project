from django.contrib.auth.models import User
from django.db import models
from django.db.models import DateField

from trainer.models import Trainer


class Student(models.Model):

    gender_options = [
        ('male', 'Male'),
        ('female', 'Female')
    ]

    first_name = models.CharField(max_length=40)  # max_length=255
    last_name = models.CharField(max_length=40, null=True, blank=True)
    profile = models.ImageField(upload_to='profiles_student/', null=True)
    email = models.EmailField(max_length=50)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=6, choices=gender_options)
    description = models.TextField(max_length=500)
    start_date = models.DateField()
    end_date = models.DateField()
    active = models.BooleanField(default=True)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Stochez data si ora cand a fost adaugat noul student
    # FARA SA SE MAI SCHIMBE DATA SI ORA
    updated_at = models.DateTimeField(auto_now=True)  # Stochez data si ora de fiecare data cand actualizez
    # studentul adaugat

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Book(models.Model):
    title = models.CharField(max_length=100, null=True)
    author = models.CharField(max_length=50, null=True)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, null=True)
    price = models.IntegerField()

    def __str__(self):
        return f'{self.title} {self.author}'


class HistoryStudent(models.Model):
    message = models.JSONField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.user}'
