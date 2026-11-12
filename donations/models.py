from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from core.models import UUIDModel


class DonationRecord(UUIDModel):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="donation_records")
    donation_date = models.DateField()
    location = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name="+"
    )

    class Meta:
        ordering = ["-donation_date", "-created_at"]
        indexes = [models.Index(fields=["donor", "status"]), models.Index(fields=["status"])]
        constraints = [
            models.CheckConstraint(condition=models.Q(donation_date__isnull=False), name="donation_date_required"),
        ]

    def clean(self):
        if self.donation_date and self.donation_date > timezone.localdate():
            raise ValidationError({"donation_date": "A donation date cannot be in the future."})

    def __str__(self):
        return f"{self.donor} - {self.donation_date} ({self.status})"
