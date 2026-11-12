from django.conf import settings
from django.db import models

from core.choices import BloodGroup
from core.models import District, UUIDModel, Upazila


class Willingness(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    INACTIVE = "INACTIVE", "Inactive"


class MemberProfile(UUIDModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="profile")
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    whatsapp_number = models.CharField(max_length=20)
    messenger_url = models.URLField(max_length=300)
    district = models.ForeignKey(District, on_delete=models.PROTECT, related_name="members")
    upazila = models.ForeignKey(Upazila, on_delete=models.PROTECT, related_name="members")
    area = models.CharField("Area / village / road", max_length=150)
    profile_image = models.ImageField(upload_to="profiles/", blank=True)
    wants_to_donate = models.BooleanField("I want to donate blood", default=False)
    needs_blood = models.BooleanField("I may need blood", default=False)
    blood_group = models.CharField(max_length=3, choices=BloodGroup.choices, blank=True)
    never_donated = models.BooleanField("I have never donated blood", default=False)
    confirmed_last_donation_date = models.DateField("Last donation date", null=True, blank=True)
    donation_willingness = models.CharField(
        max_length=8, choices=Willingness.choices, default=Willingness.ACTIVE
    )

    class Meta:
        indexes = [
            models.Index(fields=["blood_group"]),
            models.Index(fields=["district"]),
            models.Index(fields=["upazila"]),
            models.Index(fields=["donation_willingness"]),
        ]

    @property
    def masked_name(self):
        parts = self.full_name.split()
        if not parts:
            return "Member"
        return f"{parts[0]} {parts[-1][0].upper()}." if len(parts) > 1 else parts[0]

    def __str__(self):
        return self.full_name


class MemberPrivacy(UUIDModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="privacy")
    show_phone = models.BooleanField("Show my phone number to logged-in members", default=False)
    show_whatsapp = models.BooleanField("Allow WhatsApp contact", default=False)
    show_messenger = models.BooleanField("Allow Messenger contact", default=False)
    show_donation_history = models.BooleanField("Show my completed donations", default=False)
    show_area = models.BooleanField("Show my area (and allow area search)", default=False)
    allow_direct_requests = models.BooleanField("Receive direct donation requests", default=False)

    class Meta:
        verbose_name_plural = "member privacy settings"

    def snapshot(self):
        return {f: getattr(self, f) for f in PRIVACY_FIELDS}


PRIVACY_FIELDS = [
    "show_phone", "show_whatsapp", "show_messenger", "show_donation_history", "show_area", "allow_direct_requests",
]
