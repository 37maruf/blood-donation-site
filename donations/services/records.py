from moderation.services import audit

TRACKED = ("donor_id", "donation_date", "location", "status", "notes")


def snapshot(record):
    return {f: str(getattr(record, f)) for f in TRACKED}


def audit_record_change(request, record, old_snapshot):
    action = "donation_record.updated" if old_snapshot else "donation_record.created"
    audit(request.user, action, "DONATION", record.pk, {"old": old_snapshot, "new": snapshot(record)}, request)
