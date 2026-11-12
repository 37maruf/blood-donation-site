"""The Python rule and the SQL queryset must agree on every case."""
from datetime import timedelta

import pytest
from django.utils import timezone

from donations.models import DonationRecord
from donations.services.eligibility import available_queryset, evaluate

pytestmark = pytest.mark.django_db
today = lambda: timezone.localdate()  # noqa: E731


def _both(profile):
    return evaluate(profile).available, available_queryset().filter(pk=profile.pk).exists()


def test_never_donated_is_available(make_member):
    assert _both(make_member(never=True)) == (True, True)


def test_no_history_not_listed(make_member):
    assert _both(make_member(never=False, last=None)) == (False, False)


def test_59_days_not_available_60_available(make_member):
    p59 = make_member(never=False, last=today() - timedelta(days=59))
    p60 = make_member(never=False, last=today() - timedelta(days=60))
    assert _both(p59) == (False, False)
    assert _both(p60) == (True, True)


def test_completed_record_overrides_never_donated(make_member, record):
    p = make_member(never=True)
    record(p, 10)
    assert _both(p) == (False, False)


def test_effective_last_is_max_of_record_and_profile(make_member, record):
    p = make_member(never=False, last=today() - timedelta(days=200))
    record(p, 30)
    assert _both(p) == (False, False)
    p2 = make_member(never=False, last=today() - timedelta(days=20))
    record(p2, 300)
    assert _both(p2) == (False, False)


def test_pending_and_cancelled_ignored(make_member, record):
    p = make_member(never=True)
    record(p, 5, DonationRecord.Status.PENDING)
    record(p, 5, DonationRecord.Status.CANCELLED)
    assert _both(p) == (True, True)


def test_inactive_and_non_donor_excluded(make_member):
    assert _both(make_member(willingness="INACTIVE")) == (False, False)
    assert _both(make_member(donor=False)) == (False, False)
    assert _both(make_member(active=False)) == (False, False)


def test_future_date_never_available(make_member):
    p = make_member(never=False, last=today() + timedelta(days=3))
    assert _both(p) == (False, False)
