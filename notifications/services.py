from django.db.models import Exists, OuterRef, Q
from django.shortcuts import get_object_or_404
from django.urls import reverse

from .models import Notification, NotificationRead


def notify(recipient, kind, title, body="", target_type="", target_id=None, actor=None):
    return Notification.objects.create(
        recipient=recipient, actor=actor, kind=kind, title=title[:160], body=body[:600],
        target_type=target_type, target_id=target_id,
    )


def broadcast(kind, title, body="", target_type="", target_id=None, actor=None):
    """One row for everybody (recipient=NULL): no per-user fan-out."""
    return notify(None, kind, title, body, target_type, target_id, actor)


def visible_for(user):
    return Notification.objects.filter(
        Q(recipient=user) | Q(recipient__isnull=True, created_at__gte=user.date_joined)
    )


def with_read_flag(queryset, user):
    return queryset.annotate(
        is_read=Exists(NotificationRead.objects.filter(notification=OuterRef("pk"), user=user))
    )


def unread_count(user):
    return with_read_flag(visible_for(user), user).filter(is_read=False).count()


def mark_read(user, pk):
    notification = get_object_or_404(visible_for(user), pk=pk)
    NotificationRead.objects.get_or_create(notification=notification, user=user)
    return notification


def target_url(notification):
    """Only internal, reversed URLs - never user-supplied strings."""
    kind, tid = notification.target_type, notification.target_id
    if kind == "need" and tid:
        return reverse("blood_requests:need_detail", args=[tid])
    if kind == "campaign" and tid:
        return reverse("campaigns:detail", args=[tid])
    if kind == "requests_received":
        return reverse("blood_requests:request_received")
    if kind == "requests_sent":
        return reverse("blood_requests:request_sent")
    if kind == "general_request":
        return reverse("blood_requests:general_mine")
    return ""
