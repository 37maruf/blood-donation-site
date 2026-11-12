"""Single source of truth for donor availability (R2).

`evaluate()` (Python) and `available_queryset()` (SQL) implement the SAME rule and are
covered by the same tests (tests/test_eligibility.py).

available = active account AND wants_to_donate AND willingness ACTIVE AND
            ( no donation history AND never_donated  OR  days since effective_last >= 60 )
effective_last = MAX(latest COMPLETED record date, profile confirmed date). PENDING/CANCELLED ignored.
"""
from dataclasses import dataclass
from datetime import date, timedelta

from django.conf import settings
from django.db.models import DateField, Max, OuterRef, Q, Subquery
from django.db.models.functions import Greatest
from django.utils import timezone

from donations.models import DonationRecord
from members.models import MemberProfile, Willingness

DISCLAIMER = (
    "Availability follows this website's 60-day rule only. It is not medical clearance - "
    "blood centres decide who can donate."
)

MESSAGES = {
    "available": "Available to donate.",
    "interval": "Willing to donate, not currently listed under the 60-day rule.",
    "willingness_inactive": "Set to inactive: hidden from donor lists and direct requests.",
    "not_donor": "Turn on 'I want to donate' in your profile to be listed.",
    "no_history": "Confirm your donation history (never donated, or your last donation date) to be listed.",
    "inactive_account": "This account is inactive.",
}


@dataclass(frozen=True)
class Eligibility:
    available: bool
    reason: str
    effective_last: date | None = None
    next_eligible: date | None = None

    @property
    def message(self):
        return MESSAGES[self.reason]


def interval_days():
    return settings.DONATION_INTERVAL_DAYS


def effective_last_donation(profile):
    latest = DonationRecord.objects.filter(
        donor_id=profile.user_id, status=DonationRecord.Status.COMPLETED
    ).aggregate(m=Max("donation_date"))["m"]
    dates = [d for d in (latest, profile.confirmed_last_donation_date) if d]
    return max(dates) if dates else None


def evaluate(profile, today=None):
    today = today or timezone.localdate()
    user = profile.user
    if not user.is_active:
        return Eligibility(False, "inactive_account")
    if not profile.wants_to_donate:
        return Eligibility(False, "not_donor")
    if profile.donation_willingness != Willingness.ACTIVE:
        return Eligibility(False, "willingness_inactive")
    last = effective_last_donation(profile)
    if last is None:
        if profile.never_donated:
            return Eligibility(True, "available")
        return Eligibility(False, "no_history")
    next_date = last + timedelta(days=interval_days())
    if today >= next_date:
        return Eligibility(True, "available", last, next_date)
    return Eligibility(False, "interval", last, next_date)


def is_available(profile, today=None):
    return evaluate(profile, today).available


def available_queryset(today=None):
    """SQL equivalent of evaluate(); use BEFORE pagination."""
    today = today or timezone.localdate()
    cutoff = today - timedelta(days=interval_days())
    latest_completed = (
        DonationRecord.objects.filter(donor_id=OuterRef("user_id"), status=DonationRecord.Status.COMPLETED)
        .order_by("-donation_date")
        .values("donation_date")[:1]
    )
    return (
        MemberProfile.objects.filter(
            user__is_active=True,
            wants_to_donate=True,
            donation_willingness=Willingness.ACTIVE,
        )
        .annotate(latest_completed=Subquery(latest_completed, output_field=DateField()))
        # PostgreSQL GREATEST ignores NULLs, matching the Python max() over non-null dates
        .annotate(effective_last=Greatest("latest_completed", "confirmed_last_donation_date"))
        .filter(Q(effective_last__isnull=True, never_donated=True) | Q(effective_last__lte=cutoff))
        .select_related("user", "user__privacy", "district", "upazila")
    )
