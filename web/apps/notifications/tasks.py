from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from apps.applications.models import Application
from django.contrib.auth import get_user_model

User = get_user_model()

@shared_task
def send_application_notification_task(user_id, application_id, status_change=False):
    try:
        user = User.objects.get(id=user_id)
        application = Application.objects.get(id=application_id)
        
        subject = "Job Application Update" if status_change else "New Application Created"
        message = (
            f"Hello {user.username},\n\n"
            f"Your application for {application.role} at {application.company} has been updated.\n"
            f"Current Status: {application.status}\n\n"
            f"Check it out here: http://app.localhost/api/docs/"
        )
        
        send_mail(
            subject=subject,
            message=message,
            from_email='notifications@jobtracker.local',
            recipient_list=[user.email],
            fail_silently=False,
        )
        return f"Notification sent to {user.email}"
    except (User.DoesNotExist, Application.DoesNotExist):
        return "User or Application not found"

@shared_task
def check_stale_applications_task():
    stale_date = timezone.now() - timedelta(days=7)
    stale_applications = Application.objects.filter(updated_at__lte=stale_date).exclude(status__in=['rejected', 'ghosted', 'offer'])
    
    count = 0
    for app in stale_applications:
        send_mail(
            subject="Action Required: Stale Application",
            message=(
                f"Hello {app.user.username},\n\n"
                f"You haven't updated your application for {app.role} at {app.company} in over 7 days.\n"
                f"Maybe it's time to follow up?\n\n"
                f"Status: {app.status}"
            ),
            from_email='reminders@jobtracker.local',
            recipient_list=[app.user.email],
            fail_silently=False,
        )
        count += 1
    
    return f"Sent {count} stale application reminders"
