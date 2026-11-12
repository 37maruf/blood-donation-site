from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models

from core.models import UUIDModel


class Report(UUIDModel):
    class TargetType(models.TextChoices):
        USER = "USER", "Member"
        POST = "POST", "Blood need post"

    class Reason(models.TextChoices):
        SPAM = "SPAM", "Spam or scam"
        FAKE = "FAKE", "Fake or misleading"
        ABUSE = "ABUSE", "Abusive behaviour"
        PRIVACY = "PRIVACY", "Privacy concern"
        OTHER = "OTHER", "Other"

    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        REVIEWED = "REVIEWED", "Reviewed"
        ACTIONED = "ACTIONED", "Action taken"
        DISMISSED = "DISMISSED", "Dismissed"

    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="reports_made")
    target_type = models.CharField(max_length=8, choices=TargetType.choices)
    target_id = models.UUIDField()
    reason = models.CharField(max_length=10, choices=Reason.choices)
    details = models.TextField(blank=True, max_length=1000)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.OPEN)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name="reports_reviewed"
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["status"])]

    def __str__(self):
        return f"{self.get_target_type_display()} report ({self.status})"


class AuditLog(UUIDModel):
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name="audit_entries"
    )
    action = models.CharField(max_length=60, db_index=True)
    target_type = models.CharField(max_length=40, blank=True)
    target_id = models.CharField(max_length=64, blank=True)
    metadata = models.JSONField(default=dict, blank=True, encoder=DjangoJSONEncoder)
    ip_hash = models.CharField(max_length=64, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.action} @ {self.created_at:%Y-%m-%d %H:%M}"
