from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    ROLE_CHOICES = (
        ('engineer', 'Engineer'),
        ('user', 'User')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    basic_info = models.CharField(max_length=500, blank=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    is_approved = models.BooleanField(default=False)

# Służy do wyświetlania w panelu administracyjnym profilu po nazwie użytkownika    
    def __str__(self):
        return self.user.username


