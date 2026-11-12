from django.conf import settings
from django.db import transaction
from django.utils import timezone

from members.models import MemberPrivacy
from moderation.services import audit

from .models import User


@transaction.atomic
def register_member(cleaned, profile):
    """User + profile + privacy in one transaction. `profile` is an unsaved MemberProfile."""
    now = timezone.now()
    user = User.objects.create_user(
        email=cleaned["email"],
        password=cleaned["password1"],
        terms_version=settings.TERMS_VERSION,
        terms_accepted_at=now,
    )
    profile.user = user
    profile.save()
    MemberPrivacy.objects.create(user=user)
    audit(user, "user.registered", "USER", user.pk, {"terms_version": settings.TERMS_VERSION})
    return user


def change_email(request, user, new_email):
    old = user.email
    user.email = new_email.lower()
    user.save(update_fields=["email", "updated_at"])
    audit(user, "email.changed", "USER", user.pk, {"old": old, "new": user.email}, request)


def deactivate_account(request, user):
    user.is_active = False
    user.save(update_fields=["is_active", "updated_at"])
    audit(user, "user.deactivated", "USER", user.pk, {"by": "member"}, request)
