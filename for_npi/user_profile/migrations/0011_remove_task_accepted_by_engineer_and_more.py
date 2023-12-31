# Generated by Django 4.2.7 on 2023-11-16 23:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_profile', '0010_alter_task_assigned_to'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='accepted_by_engineer',
        ),
        migrations.RemoveField(
            model_name='task',
            name='accepted_by_supervisor',
        ),
        migrations.RemoveField(
            model_name='task',
            name='completed_by',
        ),
        migrations.AlterField(
            model_name='task',
            name='assigned_to',
            field=models.ManyToManyField(blank=True, null=True, related_name='assigned_tasks', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='ProductionIssue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('report_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('open', 'Open'), ('closed', 'Closed')], default='open', max_length=50)),
                ('priority', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='medium', max_length=50)),
                ('reported_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reported_issues', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
