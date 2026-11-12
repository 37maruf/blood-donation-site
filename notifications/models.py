from django.conf import settings
from django.db import models

from core.models import UUIDModel


class Notification(UUIDModel):
    class Kind(models.TextChoices):
        NEW_BLOOD_NEED = "NEW_BLOOD_NEED", "New blood need"
        DIRECT_REQUEST_RECEIVED = "DIRECT_REQUEST_RECEIVED", "Direct request received"
        DIRECT_REQUEST_ACCEPTED = "DIRECT_REQUEST_ACCEPTED", "Direct request accepted"
        DIRECT_REQUEST_REJECTED = "DIRECT_REQUEST_REJECTED", "Direct request rejected"
        DIRECT_REQUEST_CANCELLED = "DIRECT_REQUEST_CANCELLED", "Direct request cancelled"
        DIRECT_REQUEST_COMPLETED = "DIRECT_REQUEST_COMPLETED", "Direct request completed"
        NEED_RESPONSE = "NEED_RESPONSE", "Response to your blood need"
        GENERAL_REQUEST_UPDATED = "GENERAL_REQUEST_UPDATED", "General request updated"
        CAMPAIGN_UPDATE = "CAMPAIGN_UPDATE", "Campaign update"
        ANNOUNCEMENT = "ANNOUNCEMENT", "Announcement"

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name="notifications",
        help_text="Leave empty to broadcast to all members.",
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name="+"
    )
    kind = models.CharField(max_length=30, choices=Kind.choices)
    title = models.CharField(max_length=160)
    body = models.TextField(blank=True, max_length=600)
    target_type = models.CharField(max_length=40, blank=True)
    target_id = models.UUIDField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["recipient"]), models.Index(fields=["-created_at"])]

    def __str__(self):
        return self.title


class NotificationRead(UUIDModel):
    notification = models.ForeignKey(Notification, on_delete=models.PROTECT, related_name="reads")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="+")
    read_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["notification", "user"], name="notification_read_once")]
