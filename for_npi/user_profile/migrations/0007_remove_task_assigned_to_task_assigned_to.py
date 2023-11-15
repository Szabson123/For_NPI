# Generated by Django 4.2.7 on 2023-11-15 18:12

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_profile', '0006_task_assigned_to'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='assigned_to',
        ),
        migrations.AddField(
            model_name='task',
            name='assigned_to',
            field=models.ManyToManyField(blank=True, null=True, related_name='assigned_tasks', to=settings.AUTH_USER_MODEL),
        ),
    ]
