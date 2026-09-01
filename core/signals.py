from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import Profile
from .models import KorvaAIConfig


@receiver(post_save, sender=Profile)
def create_ai_config(sender, instance, created, **kwargs):
    if created:
        KorvaAIConfig.objects.get_or_create(user=instance)
