from django.db import models


class Product(models.Model):
    name = models.TextField(max_length=500)
    price = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name} - {self.price}'
