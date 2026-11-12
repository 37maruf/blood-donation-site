import hashlib
from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from .models import ThrottleHit


def client_ip(request):
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "")


def hash_value(value):
    return hashlib.sha256(f"{settings.SECRET_KEY}:{value}".encode()).hexdigest()[:32]


def allow(scope, ident, limit, seconds):
    """Record a hit and return True if the caller is still under the limit."""
    key = f"{scope}:{hash_value(ident)}"
    since = timezone.now() - timedelta(seconds=seconds)
    if ThrottleHit.objects.filter(key=key, created_at__gte=since).count() >= limit:
        return False
    ThrottleHit.objects.create(key=key)
    return True


def purge(older_than_hours=48):
    cutoff = timezone.now() - timedelta(hours=older_than_hours)
    deleted, _ = ThrottleHit.objects.filter(created_at__lt=cutoff).delete()
    return deleted
