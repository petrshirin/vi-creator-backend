from django.dispatch import receiver
from django.db.models.signals import post_save
from core.models import User
from .models import UserExecuteSettings


@receiver(post_save, sender=User)
def add_execute_settings(sender, instance, **kwargs):
    UserExecuteSettings.objects.get_or_create(user=instance)
