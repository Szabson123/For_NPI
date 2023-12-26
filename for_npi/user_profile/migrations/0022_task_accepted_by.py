# Generated by Django 4.2.7 on 2023-12-15 13:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_profile', '0021_delete_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='accepted_by',
            field=models.ManyToManyField(blank=True, related_name='accepted_tasks', to=settings.AUTH_USER_MODEL),
        ),
    ]
