from django.db import transaction
from django.utils import timezone

from core.exceptions import ServiceError
from notifications import services as notifications
from notifications.models import Notification

from .models import Campaign, CampaignRegistration


def public_campaigns():
    return Campaign.objects.filter(status=Campaign.Status.PUBLISHED)


def filter_by_phase(qs, phase):
    now = timezone.now()
    if phase == "upcoming":
        return qs.filter(starts_at__gt=now).order_by("starts_at")
    if phase == "ongoing":
        return qs.filter(starts_at__lte=now, ends_at__gte=now).order_by("ends_at")
    if phase == "past":
        return qs.filter(ends_at__lt=now).order_by("-ends_at")
    return qs.order_by("-starts_at")


def upcoming_campaigns(limit=3):
    now = timezone.now()
    return list(public_campaigns().filter(ends_at__gte=now).order_by("starts_at")[:limit])


@transaction.atomic
def register_member(campaign_id, member):
    campaign = Campaign.objects.select_for_update().get(pk=campaign_id, status=Campaign.Status.PUBLISHED)
    if campaign.ends_at < timezone.now():
        raise ServiceError("This campaign has already ended.")
    existing = CampaignRegistration.objects.filter(campaign=campaign, member=member).first()
    if existing and existing.status == CampaignRegistration.Status.REGISTERED:
        raise ServiceError("You are already registered for this campaign.")
    if campaign.capacity is not None:
        taken = campaign.registrations.filter(status=CampaignRegistration.Status.REGISTERED).count()
        if taken >= campaign.capacity:
            raise ServiceError("Sorry, this campaign is full.")
    if existing:
        existing.status = CampaignRegistration.Status.REGISTERED
        existing.save(update_fields=["status", "updated_at"])
        return existing
    return CampaignRegistration.objects.create(campaign=campaign, member=member)


def notify_registrants(campaign, what_changed, actor=None):
    """One notification per registrant (registrant lists are small and scoped)."""
    registrants = campaign.registrations.filter(status=CampaignRegistration.Status.REGISTERED).select_related("member")
    rows = [
        Notification(
            recipient=reg.member, actor=actor, kind=Notification.Kind.CAMPAIGN_UPDATE,
            title=f"Update: {campaign.title}"[:160], body=f"Changed: {what_changed}."[:600],
            target_type="campaign", target_id=campaign.pk,
        )
        for reg in registrants
    ]
    Notification.objects.bulk_create(rows)
    return len(rows)
