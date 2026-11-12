import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_default_language_is_english(client):
    html = client.get(reverse("core:home")).content.decode()
    assert '<html lang="en"' in html and "Find a donor" in html


def test_language_switch_sets_cookie_and_renders_bangla(client):
    r = client.get(reverse("core:set_language", args=["bn"]), {"next": "/about/"})
    assert r.status_code == 302 and r.url == "/about/"
    assert client.cookies["lang"].value == "bn"
    html = client.get(reverse("core:home")).content.decode()
    assert '<html lang="bn"' in html and "দাতা খুঁজুন" in html


def test_language_switch_rejects_open_redirect_and_bad_codes(client):
    r = client.get(reverse("core:set_language", args=["en"]), {"next": "https://evil.example/"})
    assert r.url == "/"
    assert client.get(reverse("core:set_language", args=["fr"])).status_code == 404


def test_browser_preferring_bangla_gets_bangla_first(client):
    html = client.get(reverse("core:home"), HTTP_ACCEPT_LANGUAGE="bn-BD,bn;q=0.9").content.decode()
    assert '<html lang="bn"' in html


def test_theme_toggle_present_and_theme_attribute_set(client):
    html = client.get(reverse("core:home")).content.decode()
    assert 'id="theme-toggle"' in html and 'data-bs-theme="' in html


def test_form_labels_and_choices_are_translated(client):
    client.cookies["lang"] = "bn"
    html = client.get(reverse("accounts:register")).content.decode()
    assert "পূর্ণ নাম" in html and "উপজেলা বেছে নিন" in html


def test_static_pages_use_bangla_text_when_available(client):
    client.cookies["lang"] = "bn"
    assert "সূর্যতরী সম্পর্কে" in client.get(reverse("content:about")).content.decode()
