from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone

from core import throttle
from core.exceptions import RateLimited, ServiceError
from donations.services.eligibility import is_available
from moderation.services import audit
from notifications import services as notifications
from notifications.models import Notification

from .models import BloodNeedPost, BloodNeedResponse, DonationRequest, GeneralBloodRequest

K = Notification.Kind


def _limit(scope, user, limit, seconds):
    if not throttle.allow(scope, f"u{user.pk}", limit, seconds):
        raise RateLimited("You are doing that too often. Please try again later.")


# ---------------------------------------------------------------- Blood Need (public)
@transaction.atomic
def create_need_post(owner, form):
    """Post + ONE broadcast notification in the same transaction (no per-user fan-out)."""
    _limit("need_create", owner, 5, 86400)
    post = form.save(commit=False)
    post.owner = owner
    post.status = BloodNeedPost.Status.ACTIVE
    post.save()
    notifications.broadcast(
        K.NEW_BLOOD_NEED,
        f"{post.get_urgency_display()}: {post.blood_group} blood needed",
        f"{post.units} unit(s) at {post.hospital_name}, {post.hospital_location}.",
        "need", post.pk, owner,
    )
    return post


def close_need_post(post, user, new_status):
    if post.owner_id != user.pk:
        raise ServiceError("Only the owner can close this post.")
    if new_status not in (BloodNeedPost.Status.FULFILLED, BloodNeedPost.Status.CANCELLED):
        raise ServiceError("Invalid status.")
    if post.status != BloodNeedPost.Status.ACTIVE:
        raise ServiceError("This post is already closed.")
    post.status = new_status
    post.closed_at = timezone.now()
    post.save(update_fields=["status", "closed_at", "updated_at"])
    audit(user, f"need.{new_status.lower()}", "POST", post.pk)


@transaction.atomic
def respond_to_need(post, member, message=""):
    if post.is_hidden or post.status != BloodNeedPost.Status.ACTIVE:
        raise ServiceError("This request is no longer active.")
    if post.owner_id == member.pk:
        raise ServiceError("You cannot respond to your own post.")
    _limit("need_respond", member, 20, 86400)
    try:
        with transaction.atomic():
            BloodNeedResponse.objects.create(post=post, member=member, message=message[:300])
    except IntegrityError:
        raise ServiceError("You have already offered to help with this request.")
    notifications.notify(
        post.owner, K.NEED_RESPONSE, "Someone offered to donate",
        f"A member responded to your {post.blood_group} request.", "need", post.pk, member,
    )


# ---------------------------------------------------------------- General request (private)
def create_general_request(requester, form):
    _limit("general_create", requester, 5, 86400)
    req = form.save(commit=False)
    req.requester = requester
    req.status = GeneralBloodRequest.Status.SUBMITTED
    req.save()
    audit(requester, "general_request.created", "GENERAL_REQUEST", req.pk)
    return req


def notify_general_status_change(request_obj, staff_user, old_status):
    notifications.notify(
        request_obj.requester, K.GENERAL_REQUEST_UPDATED, "Your blood request was updated",
        f"Status: {request_obj.get_status_display()}.", "general_request", request_obj.pk, staff_user,
    )
    audit(staff_user, "general_request.status_changed", "GENERAL_REQUEST", request_obj.pk,
          {"old": old_status, "new": request_obj.status})


# ---------------------------------------------------------------- Direct request (private)
@transaction.atomic
def create_direct_request(requester, donor_profile, form, request=None):
    donor = donor_profile.user
    if requester.pk == donor.pk:
        raise ServiceError("You cannot send a request to yourself.")
    if not is_available(donor_profile) or not donor.privacy.allow_direct_requests:
        raise ServiceError("This donor cannot receive requests right now.")
    _limit("direct_request", requester, 5, 86400)
    if DonationRequest.objects.filter(
        requester=requester, donor=donor, status=DonationRequest.Status.PENDING
    ).exists():
        raise ServiceError("You already have a pending request to this donor.")
    obj = form.save(commit=False)
    obj.requester, obj.donor = requester, donor
    obj.blood_group = donor_profile.blood_group  # never trust a posted value
    obj.status = DonationRequest.Status.PENDING
    try:
        with transaction.atomic():
            obj.save()
    except IntegrityError:
        raise ServiceError("You already have a pending request to this donor.")
    notifications.notify(
        donor, K.DIRECT_REQUEST_RECEIVED, "New donation request",
        f"A member asked for {obj.blood_group} blood near {obj.hospital_location}.",
        "requests_received", obj.pk, requester,
    )
    audit(requester, "direct_request.created", "DONATION_REQUEST", obj.pk, request=request)
    return obj


_ACTIONS = {
    "accept": (DonationRequest.Status.ACCEPTED, K.DIRECT_REQUEST_ACCEPTED, "accepted"),
    "reject": (DonationRequest.Status.REJECTED, K.DIRECT_REQUEST_REJECTED, "rejected"),
    "cancel": (DonationRequest.Status.CANCELLED, K.DIRECT_REQUEST_CANCELLED, "cancelled"),
    "complete": (DonationRequest.Status.COMPLETED, K.DIRECT_REQUEST_COMPLETED, "completed"),
}


@transaction.atomic
def transition_direct_request(pk, actor, action, request=None):
    """State machine, row-locked. Each transition notifies the other party and writes an AuditLog."""
    if action not in _ACTIONS:
        raise ServiceError("Unknown action.")
    obj = get_object_or_404(DonationRequest.objects.select_for_update(), pk=pk)
    S = DonationRequest.Status
    is_donor, is_requester = actor.pk == obj.donor_id, actor.pk == obj.requester_id
    is_staff = actor.is_staff and actor.has_perm("blood_requests.change_donationrequest")
    if not (is_donor or is_requester or is_staff):
        raise ServiceError("You cannot change this request.")
    allowed = {
        "accept": is_donor and obj.status == S.PENDING,
        "reject": is_donor and obj.status == S.PENDING,
        "cancel": is_requester and obj.status in (S.PENDING, S.ACCEPTED),
        "complete": (is_donor or is_requester or is_staff) and obj.status == S.ACCEPTED,
    }[action]
    if not allowed:
        raise ServiceError("That action is not allowed in the request's current state.")
    new_status, kind, verb = _ACTIONS[action]
    old_status = obj.status
    obj.status = new_status
    now = timezone.now()
    if action in ("accept", "reject"):
        obj.responded_at = now
    if action == "complete":
        obj.completed_at = now
    obj.save(update_fields=["status", "responded_at", "completed_at", "updated_at"])
    recipients = {obj.requester_id: ("requests_sent", obj.requester), obj.donor_id: ("requests_received", obj.donor)}
    for uid, (target, user) in recipients.items():
        if uid != actor.pk:
            notifications.notify(user, kind, f"Donation request {verb}", "", target, obj.pk, actor)
    audit(actor, f"direct_request.{verb}", "DONATION_REQUEST", obj.pk, {"old": old_status, "new": new_status}, request)
    return obj
