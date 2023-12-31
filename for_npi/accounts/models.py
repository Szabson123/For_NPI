from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    ROLE_CHOICES = (
        ('engineer', 'Engineer'),
        ('user', 'User'),
        ('production', 'Production'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    basic_info = models.CharField(max_length=500, blank=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    is_approved = models.BooleanField(default=False)
    supervisor = models.ForeignKey(User, related_name='engineers', on_delete=models.SET_NULL, null=True, blank=True)
    position = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    office_number = models.CharField(max_length=20, blank=True)
    languages = models.CharField(max_length=100, blank=True)

# Służy do wyświetlania w panelu administracyjnym profilu po nazwie użytkownika    
    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def assign_user_group(sender, instance, created, **kwargs):
    if created and hasattr(instance, 'profile'):
        role = instance.profile.role
        group_name = role.capitalize()  # Używamy metody capitalize(), aby mieć pewność, że nazwa grupy zaczyna się z wielkiej litery.
        group, _ = Group.objects.get_or_create(name=group_name)
        instance.groups.add(group)
