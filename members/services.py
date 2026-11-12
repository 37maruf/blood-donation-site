from django.db import transaction

from donations.services.eligibility import available_queryset
from moderation.services import audit

from .models import PRIVACY_FIELDS


def search_donors(blood_group="", upazila=None, area=""):
    """Filters run on the eligibility queryset BEFORE pagination."""
    qs = available_queryset()
    if blood_group:
        qs = qs.filter(blood_group=blood_group)
    if upazila:
        qs = qs.filter(upazila=upazila)
    if area:
        # only donors who chose to show their area can be matched by area
        qs = qs.filter(user__privacy__show_area=True, area__icontains=area.strip())
    return qs.order_by("blood_group", "upazila__name", "id")


@transaction.atomic
def save_profile(request, form):
    profile = form.save()
    audit(request.user, "profile.updated", "USER", request.user.pk, {"fields": sorted(form.changed_data)}, request)
    return profile


@transaction.atomic
def update_donation_settings(request, profile, cleaned):
    old = {
        "willingness": profile.donation_willingness,
        "never_donated": profile.never_donated,
        "last_donation": profile.confirmed_last_donation_date,
    }
    profile.donation_willingness = cleaned["donation_willingness"]
    profile.never_donated = bool(cleaned.get("never_donated"))
    profile.confirmed_last_donation_date = cleaned.get("confirmed_last_donation_date")
    profile.save(update_fields=["donation_willingness", "never_donated", "confirmed_last_donation_date", "updated_at"])
    new = {
        "willingness": profile.donation_willingness,
        "never_donated": profile.never_donated,
        "last_donation": profile.confirmed_last_donation_date,
    }
    if old != new:
        audit(request.user, "donation_settings.changed", "USER", request.user.pk, {"old": old, "new": new}, request)


@transaction.atomic
def update_privacy(request, form, old):
    """`old` must be captured BEFORE binding the form (validation mutates the instance)."""
    privacy = form.save()
    new = {f: getattr(privacy, f) for f in PRIVACY_FIELDS}
    if old != new:
        audit(request.user, "privacy.changed", "USER", request.user.pk, {"old": old, "new": new}, request)
    return privacy
