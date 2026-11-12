import uuid

from django.db import models
from django.utils import timezone, translation


def _localized_name(obj):
    if (translation.get_language() or "en").startswith("bn") and obj.name_bn:
        return obj.name_bn
    return obj.name


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class District(UUIDModel):
    name = models.CharField(max_length=80, unique=True)
    name_bn = models.CharField(max_length=80, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return _localized_name(self)


class Upazila(UUIDModel):
    district = models.ForeignKey(District, on_delete=models.PROTECT, related_name="upazilas")
    name = models.CharField(max_length=80)
    name_bn = models.CharField(max_length=80, blank=True)

    class Meta:
        ordering = ["name"]
        constraints = [models.UniqueConstraint(fields=["district", "name"], name="upazila_unique_in_district")]

    def __str__(self):
        return _localized_name(self)


class ThrottleHit(models.Model):
    """DB-backed rate limiting (works on serverless; Redis is optional)."""

    key = models.CharField(max_length=120, db_index=True)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
