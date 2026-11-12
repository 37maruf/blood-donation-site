from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone

from blood_requests.models import BloodNeedPost, DonationRequest
from core.exceptions import ServiceError
from blood_requests import services
from notifications.models import Notification

pytestmark = pytest.mark.django_db


def need_payload(**over):
    data = {
        "patient_name": "Patient", "blood_group": "B+", "units": 2, "hospital_name": "Rajbari Sadar Hospital",
        "hospital_location": "Rajbari", "required_date": (timezone.localdate() + timedelta(days=2)).isoformat(),
        "contact_phone": "01711111111", "urgency": "URGENT", "details": "Please help",
    }
    data.update(over)
    return data


def test_need_creates_post_and_single_broadcast(client, make_member):
    owner = make_member(donor=False)
    for _ in range(5):
        make_member()
    client.force_login(owner.user)
    r = client.post(reverse("blood_requests:need_create"), need_payload())
    assert r.status_code == 302
    assert BloodNeedPost.objects.count() == 1
    assert Notification.objects.filter(kind="NEW_BLOOD_NEED", recipient__isnull=True).count() == 1


def test_public_summary_hides_patient_and_contact(client, make_member):
    owner = make_member(donor=False)
    client.force_login(owner.user)
    client.post(reverse("blood_requests:need_create"), need_payload())
    client.logout()
    post = BloodNeedPost.objects.get()
    html = client.get(reverse("blood_requests:need_detail", args=[post.pk])).content.decode()
    assert "01711111111" not in html  # contact_public is off by default
    assert "Patient" not in html  # patient_name_public is off by default


def test_new_member_can_post_without_email_verification(client, make_member):
    owner = make_member(donor=False)
    client.force_login(owner.user)
    client.post(reverse("blood_requests:need_create"), need_payload())
    assert BloodNeedPost.objects.count() == 1


def test_direct_request_flow(make_member):
    donor = make_member(allow_direct_requests=True)
    requester = make_member(donor=False)

    class F:  # minimal stand-in for a bound ModelForm
        def save(self, commit=False):
            return DonationRequest(hospital_location="Rajbari", required_date=timezone.localdate())

    req = services.create_direct_request(requester.user, donor, F())
    with pytest.raises(ServiceError):  # duplicate PENDING
        services.create_direct_request(requester.user, donor, F())
    with pytest.raises(ServiceError):  # requester cannot accept
        services.transition_direct_request(req.pk, requester.user, "accept")
    services.transition_direct_request(req.pk, donor.user, "accept")
    services.transition_direct_request(req.pk, requester.user, "complete")
    req.refresh_from_db()
    assert req.status == "COMPLETED"
    assert Notification.objects.filter(recipient=requester.user, kind="DIRECT_REQUEST_ACCEPTED").exists()


def test_direct_request_needs_donor_opt_in(make_member):
    donor = make_member()  # allow_direct_requests defaults to False
    requester = make_member(donor=False)

    class F:
        def save(self, commit=False):
            return DonationRequest(hospital_location="x", required_date=timezone.localdate())

    with pytest.raises(ServiceError):
        services.create_direct_request(requester.user, donor, F())
