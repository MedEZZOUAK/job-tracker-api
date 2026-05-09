from django.db import models
from django.conf import settings

import uuid
import os

def user_resume_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('resumes', f"user_{instance.user.id}", filename)

class Application(models.Model):
    STATUS_CHOICES = [
        ("applied", "Applied"),
        ("interview", "Interview"),
        ("offer", "Offer"),
        ("rejected", "Rejected"),
        ("ghosted", "Ghosted"),
    ]

    user         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    company      = models.CharField(max_length=255)
    role         = models.CharField(max_length=255)
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES, default="applied")
    location     = models.CharField(max_length=255, blank=True)
    url          = models.URLField(blank=True)
    notes        = models.TextField(blank=True)
    applied_at   = models.DateField()
    updated_at   = models.DateTimeField(auto_now=True)
    resume       = models.FileField(upload_to=user_resume_path, null=True, blank=True)

    def __str__(self):
        return f"{self.role} at {self.company}"

class ApplicationNote(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='application_notes')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note for {self.application} at {self.created_at}"

class StatusChange(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='timeline')
    from_status = models.CharField(max_length=20)
    to_status = models.CharField(max_length=20)
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.application}: {self.from_status} -> {self.to_status}"
