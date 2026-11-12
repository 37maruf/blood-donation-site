from django.utils import timezone

from core.throttle import client_ip, hash_value

from .models import AuditLog


def audit(actor, action, target_type="", target_id="", metadata=None, request=None):
    ip_hash = hash_value(client_ip(request)) if request is not None else ""
    return AuditLog.objects.create(
        actor=actor if getattr(actor, "pk", None) else None,
        action=action,
        target_type=target_type,
        target_id=str(target_id or ""),
        metadata=metadata or {},
        ip_hash=ip_hash,
    )


def hide_post(post, staff_user, reason, request=None):
    post.is_hidden = True
    post.hidden_reason = reason[:200]
    post.save(update_fields=["is_hidden", "hidden_reason", "updated_at"])
    audit(staff_user, "post.hidden", "POST", post.pk, {"reason": reason}, request)


def mark_reviewed(report, staff_user, status):
    report.status = status
    report.reviewed_by = staff_user
    report.reviewed_at = timezone.now()
    report.save(update_fields=["status", "reviewed_by", "reviewed_at", "updated_at"])
