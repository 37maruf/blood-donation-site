import re
from urllib.parse import quote

from members.validators import is_valid_messenger_url

PREFILL = "Assalamu alaikum, I found your profile on Surjotori Blood Donation. Are you able to donate blood? Thank you."


def whatsapp_digits(raw):
    digits = re.sub(r"\D", "", raw or "")
    if digits.startswith("880"):
        return digits
    if digits.startswith("0"):
        return "88" + digits
    return digits


def whatsapp_link(profile):
    digits = whatsapp_digits(profile.whatsapp_number)
    return f"https://wa.me/{digits}?text={quote(PREFILL)}" if digits else ""


def messenger_link(profile):
    return profile.messenger_url if is_valid_messenger_url(profile.messenger_url) else ""


def allowed_channels(profile, privacy):
    """Channel keys that may be rendered: donor's flag is true AND the stored value is valid."""
    channels = []
    if privacy.show_whatsapp and whatsapp_link(profile):
        channels.append("whatsapp")
    if privacy.show_messenger and messenger_link(profile):
        channels.append("messenger")
    return channels


def link_for(profile, channel):
    return whatsapp_link(profile) if channel == "whatsapp" else messenger_link(profile)
