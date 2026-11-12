import re
from urllib.parse import urlparse

from django.core.exceptions import ValidationError

BD_PHONE_RE = re.compile(r"^(?:\+?88)?01[3-9]\d{8}$")
MESSENGER_HOSTS = ("facebook.com", "fb.com", "m.me", "messenger.com")


def normalize_phone(raw):
    return re.sub(r"[\s\-()]", "", raw or "")


def validate_bd_phone(value):
    if not BD_PHONE_RE.match(normalize_phone(value)):
        raise ValidationError("Enter a valid Bangladeshi mobile number, e.g. 01XXXXXXXXX.")


def is_valid_messenger_url(value):
    try:
        parsed = urlparse((value or "").strip())
        host = (parsed.hostname or "").lower()
    except ValueError:
        return False
    if parsed.scheme not in ("https", "http"):
        return False
    return any(host == h or host.endswith("." + h) for h in MESSENGER_HOSTS)


def validate_messenger_url(value):
    if not is_valid_messenger_url(value):
        raise ValidationError("Use a link from facebook.com, fb.com, m.me or messenger.com.")


def donor_history_errors(never_donated, last_date, today):
    """Exactly one of never_donated / last date; date not in the future."""
    errors = []
    if never_donated and last_date:
        errors.append(("confirmed_last_donation_date", "Choose either 'never donated' or a last donation date, not both."))
    elif not never_donated and not last_date:
        errors.append(("confirmed_last_donation_date", "Tell us your last donation date, or tick 'never donated'."))
    if last_date and last_date > today:
        errors.append(("confirmed_last_donation_date", "The last donation date cannot be in the future."))
    return errors
