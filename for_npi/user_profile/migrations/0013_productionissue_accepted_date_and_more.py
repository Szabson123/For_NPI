# Generated by Django 4.2.7 on 2023-11-19 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0012_productionissue_assigned_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='productionissue',
            name='accepted_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='productionissue',
            name='completed_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
