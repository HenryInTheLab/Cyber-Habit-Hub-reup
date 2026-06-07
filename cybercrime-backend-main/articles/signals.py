from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Article

@receiver(post_save, sender=Article)
def fetch_thumbnail_on_create(sender, instance, created, **kwargs):
    if created and not instance.thumbnail_url:
        instance.fetch_thumbnail()
