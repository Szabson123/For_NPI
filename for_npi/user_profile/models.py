from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings

class Task(models.Model):
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    )

    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    accepted_date = models.DateTimeField(null=True, blank=True)
    completed_date = models.DateTimeField(null=True, blank=True)
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES)
    additional = models.CharField(max_length=255, blank=True)
    assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='assigned_tasks')

    def get_absolute_url(self):
        return reverse('user_profile:task_detail', kwargs={"pk": self.pk})


class ProductionIssue(models.Model):
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('closed', 'Closed')
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reported_issues')
    report_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='open')
    priority = models.CharField(max_length=50, choices=Task.PRIORITY_CHOICES, default='medium')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='assigned_issues')

    def __str__(self):
        return self.title