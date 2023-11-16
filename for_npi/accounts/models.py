from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    ROLE_CHOICES = (
        ('engineer', 'Engineer'),
        ('user', 'User'),
        ('production', 'Production')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    basic_info = models.CharField(max_length=500, blank=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    is_approved = models.BooleanField(default=False)
    supervisor = models.ForeignKey(User, related_name='engineers', on_delete=models.SET_NULL, null=True, blank=True)

# Służy do wyświetlania w panelu administracyjnym profilu po nazwie użytkownika    
    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def assign_user_group(sender, instance, created, **kwargs):
    if created:
        role = instance.profile.role if hasattr(instance, 'profile') else 'User'
        group_name = 'Engineer' if role == 'engineer' else 'User'
        group, _ = Group.objects.get_or_create(name=group_name)
        instance.groups.add(group)
