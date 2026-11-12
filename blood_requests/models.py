from django.conf import settings
from django.db import models

from core.choices import BloodGroup, Urgency
from core.models import UUIDModel

User = settings.AUTH_USER_MODEL


class BloodNeedPost(UUIDModel):
    """Public post (summary visible to guests). Never deleted - closed instead."""

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        FULFILLED = "FULFILLED", "Fulfilled"
        CANCELLED = "CANCELLED", "Cancelled"

    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name="blood_need_posts")
    patient_name = models.CharField(max_length=120)
    patient_name_public = models.BooleanField("Show patient name publicly", default=False)
    blood_group = models.CharField(max_length=3, choices=BloodGroup.choices)
    units = models.PositiveIntegerField(default=1)
    hospital_name = models.CharField(max_length=160)
    hospital_location = models.CharField(max_length=200)
    required_date = models.DateField()
    contact_phone = models.CharField(max_length=20)
    contact_public = models.BooleanField("Show contact number to logged-in members", default=False)
    details = models.TextField(blank=True, max_length=1500)
    urgency = models.CharField(max_length=10, choices=Urgency.choices, default=Urgency.NORMAL)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    closed_at = models.DateTimeField(null=True, blank=True)
    is_hidden = models.BooleanField(default=False)
    hidden_reason = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["blood_group"]),
            models.Index(fields=["status"]),
            models.Index(fields=["required_date"]),
        ]
        constraints = [
            models.CheckConstraint(condition=models.Q(units__gte=1), name="need_units_gte_1"),
            models.CheckConstraint(condition=models.Q(required_date__isnull=False), name="need_required_date_set"),
        ]

    def __str__(self):
        return f"{self.blood_group} x{self.units} - {self.hospital_name}"


class GeneralBloodRequest(UUIDModel):
    """Private, member-owned, admin-reviewed. Never auto-published."""

    class Status(models.TextChoices):
        SUBMITTED = "SUBMITTED", "Submitted"
        UNDER_REVIEW = "UNDER_REVIEW", "Under review"
        MATCHED = "MATCHED", "Matched"
        FULFILLED = "FULFILLED", "Fulfilled"
        CANCELLED = "CANCELLED", "Cancelled"

    requester = models.ForeignKey(User, on_delete=models.PROTECT, related_name="general_requests")
    patient_name = models.CharField(max_length=120)
    blood_group = models.CharField(max_length=3, choices=BloodGroup.choices)
    units = models.PositiveIntegerField(default=1)
    hospital = models.CharField(max_length=160)
    location = models.CharField(max_length=200)
    required_date = models.DateField()
    contact = models.CharField(max_length=20)
    message = models.TextField(blank=True, max_length=1500)
    urgency = models.CharField(max_length=10, choices=Urgency.choices, default=Urgency.NORMAL)
    status = models.CharField(max_length=14, choices=Status.choices, default=Status.SUBMITTED)
    admin_notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["requester", "status"]),
            models.Index(fields=["status"]),
            models.Index(fields=["required_date"]),
        ]
        constraints = [models.CheckConstraint(condition=models.Q(units__gte=1), name="general_units_gte_1")]

    def __str__(self):
        return f"General request {self.blood_group} ({self.status})"


class DonationRequest(UUIDModel):
    """Private request from one member to one donor."""

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        ACCEPTED = "ACCEPTED", "Accepted"
        REJECTED = "REJECTED", "Rejected"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    requester = models.ForeignKey(User, on_delete=models.PROTECT, related_name="requests_sent")
    donor = models.ForeignKey(User, on_delete=models.PROTECT, related_name="requests_received")
    blood_group = models.CharField(max_length=3, choices=BloodGroup.choices)
    hospital_location = models.CharField(max_length=200)
    required_date = models.DateField()
    message = models.TextField(blank=True, max_length=800)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    responded_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["donor", "status"]),
            models.Index(fields=["requester", "status"]),
            models.Index(fields=["required_date"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["requester", "donor"], condition=models.Q(status="PENDING"), name="one_pending_request_per_pair"
            ),
            models.CheckConstraint(condition=~models.Q(requester=models.F("donor")), name="request_not_to_self"),
        ]


class BloodNeedResponse(UUIDModel):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        WITHDRAWN = "WITHDRAWN", "Withdrawn"

    post = models.ForeignKey(BloodNeedPost, on_delete=models.PROTECT, related_name="responses")
    member = models.ForeignKey(User, on_delete=models.PROTECT, related_name="need_responses")
    message = models.CharField(max_length=300, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["post", "member"], condition=models.Q(status="ACTIVE"), name="one_active_response_per_post"
            )
        ]
