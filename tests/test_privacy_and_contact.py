import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def login(client, profile):
    client.force_login(profile.user)


def test_guest_list_shows_masked_name_only(client, make_member):
    donor = make_member()
    html = client.get(reverse("members:donor_list")).content.decode()
    assert donor.masked_name in html
    assert donor.full_name not in html and donor.phone not in html


def test_detail_requires_login(client, make_member):
    donor = make_member()
    r = client.get(reverse("members:donor_detail", args=[donor.pk]))
    assert r.status_code == 302 and "/accounts/login/" in r.url


def test_hidden_fields_never_in_html(client, make_member):
    donor, viewer = make_member(), make_member()
    login(client, viewer)
    html = client.get(reverse("members:donor_detail", args=[donor.pk])).content.decode()
    assert donor.phone not in html and "wa.me" not in html and "m.me" not in html and donor.area not in html


def test_enabled_fields_are_shown_and_contact_goes_through_post(client, make_member):
    donor = make_member(show_phone=True, show_whatsapp=True, show_area=True)
    login(client, make_member())
    html = client.get(reverse("members:donor_detail", args=[donor.pk])).content.decode()
    assert donor.phone in html and donor.area in html
    assert "wa.me" not in html  # link only appears in the redirect
    url = reverse("contacts:click", args=[donor.pk, "whatsapp"])
    assert client.get(url).status_code == 405
    r = client.post(url)
    assert r.status_code == 302 and r.url.startswith("https://wa.me/8801711111111")


def test_contact_blocked_when_flag_off(client, make_member):
    donor = make_member()
    login(client, make_member())
    assert client.post(reverse("contacts:click", args=[donor.pk, "whatsapp"])).status_code == 404


def test_area_search_only_matches_donors_who_show_area(client, make_member):
    shown = make_member(show_area=True)
    hidden = make_member()
    html = client.get(reverse("members:donor_search"), {"area": "test area"}).content.decode()
    # both test members share one masked name, so count the donor cards instead
    assert html.count('class="donor"') == 1
