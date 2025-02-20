import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Project

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Project)  # Replace with your model
def on_project_created(sender, instance, created, **kwargs):
    if created:
        print(f"A new instance of {sender.__name__} has been created with id {instance.id}")
        # Your custom logic for handling the creation of a new instance goes here
