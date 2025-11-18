"""
Django signals for API app
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserResume, ResumeTemplate


@receiver(post_save, sender=UserResume)
def increment_template_usage(sender, instance, created, **kwargs):
    """Increment template usage count when a new resume is created"""
    if created and instance.template:
        instance.template.increment_usage()
