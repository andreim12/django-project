from django.db import models


class Trainer(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    course = models.CharField(max_length=40)
    email = models.EmailField(max_length=40)
    active = models.BooleanField(default=True)
    profile = models.ImageField(upload_to='profiles_trainer/', null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
