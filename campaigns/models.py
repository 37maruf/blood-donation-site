from django.conf import settings
from django.db import models
from django.templatetags.static import static
from django.utils import timezone, translation

from core.models import District, UUIDModel


class Campaign(UUIDModel):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        PUBLISHED = "PUBLISHED", "Published"
        ARCHIVED = "ARCHIVED", "Archived"

    title = models.CharField(max_length=200)
    description = models.TextField()
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    venue = models.CharField(max_length=250)
    district = models.ForeignKey(District, on_delete=models.PROTECT, null=True, blank=True, related_name="campaigns")
    image = models.ImageField(upload_to="campaigns/", blank=True)
    static_image = models.CharField(
        max_length=200, blank=True, help_text="Optional path under /static/ used when no image is uploaded."
    )
    title_bn = models.CharField("title (Bangla)", max_length=200, blank=True)
    description_bn = models.TextField("description (Bangla)", blank=True)
    venue_bn = models.CharField("venue (Bangla)", max_length=250, blank=True)
    capacity = models.PositiveIntegerField(null=True, blank=True, help_text="Leave empty for unlimited.")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name="+"
    )

    class Meta:
        ordering = ["-starts_at"]
        indexes = [models.Index(fields=["status"]), models.Index(fields=["starts_at"])]
        constraints = [models.CheckConstraint(condition=models.Q(ends_at__gte=models.F("starts_at")), name="campaign_end_after_start")]

    @staticmethod
    def _bn():
        return (translation.get_language() or "en").startswith("bn")

    @property
    def display_title(self):
        return self.title_bn if (self._bn() and self.title_bn) else self.title

    @property
    def display_description(self):
        return self.description_bn if (self._bn() and self.description_bn) else self.description

    @property
    def display_venue(self):
        return self.venue_bn if (self._bn() and self.venue_bn) else self.venue

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        if self.static_image:
            return static(self.static_image)
        return static("img/logo.png")

    @property
    def phase(self):
        now = timezone.now()
        if self.ends_at < now:
            return "past"
        return "ongoing" if self.starts_at <= now else "upcoming"

    def __str__(self):
        return self.title


class CampaignRegistration(UUIDModel):
    class Status(models.TextChoices):
        REGISTERED = "REGISTERED", "Registered"
        CANCELLED = "CANCELLED", "Cancelled"

    campaign = models.ForeignKey(Campaign, on_delete=models.PROTECT, related_name="registrations")
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="campaign_registrations")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.REGISTERED)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["campaign", "member"], name="one_registration_per_member")]
