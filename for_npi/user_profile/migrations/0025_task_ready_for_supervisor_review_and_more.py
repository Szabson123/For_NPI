# Generated by Django 4.2.7 on 2023-12-15 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0024_taskcompletion'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='ready_for_supervisor_review',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='TaskCompletion',
        ),
    ]
