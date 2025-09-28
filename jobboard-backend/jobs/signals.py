from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Application, Notification


@receiver(post_save, sender=Application)
def create_application_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.job.created_by,
            message=f"{instance.candidate.username} applied for {instance.job.title}",
        )
