# Generated by Django 5.1 on 2024-08-26 17:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
        ('trainer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='trainer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='trainer.trainer'),
        ),
    ]
