from django.db import models
from django.utils import timezone
from django.urls import reverse


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


    def get_absolute_url(self):
        return reverse('user_profile:task_detail', kwargs={"pk": self.pk})
