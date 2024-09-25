from django.db import models


class UserHistory(models.Model):
    user_data = models.JSONField()  # Pentru stocarea datelor intr-un format JSON
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'History entry at {self.created_at}'
