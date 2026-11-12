import pytest
from django.urls import reverse

from accounts.models import User
from members.models import MemberPrivacy

pytestmark = pytest.mark.django_db


def payload(district, upazila, **over):
    data = {
        "full_name": "Rahim Uddin", "email": "Rahim@Example.com", "password1": "Str0ng-pass-phrase!",
        "password2": "Str0ng-pass-phrase!", "phone": "01712345678", "whatsapp_number": "01712345678",
        "messenger_url": "https://www.facebook.com/rahim", "district": district.pk, "upazila": upazila.pk,
        "area": "Station road", "wants_to_donate": "on", "blood_group": "A+", "never_donated": "on",
        "accept_terms": "on",
    }
    data.update(over)
    return data


def test_register_creates_user_profile_privacy(client, district, upazila):
    r = client.post(reverse("accounts:register"), payload(district, upazila))
    assert r.status_code == 302
    user = User.objects.get(email="rahim@example.com")
    assert user.profile.blood_group == "A+" and user.terms_version
    assert MemberPrivacy.objects.get(user=user).show_phone is False  # privacy defaults to OFF


def test_messenger_host_is_restricted(client, district, upazila):
    r = client.post(reverse("accounts:register"), payload(district, upazila, messenger_url="https://evil.example/x"))
    assert r.status_code == 200 and not User.objects.exists()


def test_needs_at_least_one_choice(client, district, upazila):
    data = payload(district, upazila)
    data.pop("wants_to_donate")
    r = client.post(reverse("accounts:register"), data)
    assert r.status_code == 200 and not User.objects.exists()


def test_donor_requires_blood_group_and_history(client, district, upazila):
    r = client.post(reverse("accounts:register"), payload(district, upazila, blood_group=""))
    assert not User.objects.exists()
    data = payload(district, upazila)
    data.pop("never_donated")
    client.post(reverse("accounts:register"), data)
    assert not User.objects.exists()


def test_non_donor_clears_donor_only_values(client, district, upazila):
    data = payload(district, upazila, needs_blood="on")
    data.pop("wants_to_donate")
    client.post(reverse("accounts:register"), data)
    profile = User.objects.get(email="rahim@example.com").profile
    assert profile.blood_group == "" and profile.never_donated is False


def test_new_member_is_active_immediately_without_email_verification(client, district, upazila):
    """Registering is enough: no verification step, no waiting, full member access."""
    from django.core import mail

    r = client.post(reverse("accounts:register"), payload(district, upazila))
    assert r.status_code == 302
    assert mail.outbox == []  # no verification email is sent
    user = User.objects.get(email="rahim@example.com")
    # logged in straight away and allowed into member-only pages
    assert client.get(reverse("dashboard:index")).status_code == 200
    assert client.get(reverse("blood_requests:need_create")).status_code == 200
    # and listed as an available donor right away
    from donations.services.eligibility import available_queryset

    assert available_queryset().filter(user=user).exists()
