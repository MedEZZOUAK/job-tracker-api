from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.applications.models import Application
from .tasks import send_application_notification_task

@receiver(post_save, sender=Application)
def application_saved_handler(sender, instance, created, **kwargs):
    # Trigger the async task
    send_application_notification_task.delay(
        user_id=instance.user.id,
        application_id=instance.id,
        status_change=not created
    )
