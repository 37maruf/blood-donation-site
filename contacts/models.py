from django.conf import settings
from django.db import models

from core.models import UUIDModel


class ContactAttempt(UUIDModel):
    class Channel(models.TextChoices):
        WHATSAPP = "WHATSAPP", "WhatsApp"
        MESSENGER = "MESSENGER", "Messenger"

    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="contact_attempts")
    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="+")
    channel = models.CharField(max_length=10, choices=Channel.choices)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["member", "-created_at"])]
