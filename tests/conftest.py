import itertools
from datetime import date, timedelta

import pytest
from django.utils import timezone

from accounts.models import User
from core.models import District, Upazila
from donations.models import DonationRecord
from members.models import MemberPrivacy, MemberProfile

_counter = itertools.count(1)


@pytest.fixture
def district(db):
    return District.objects.get(name="Rajbari")  # seeded after migrate


@pytest.fixture
def upazila(district):
    return Upazila.objects.filter(district=district).first()


@pytest.fixture
def make_member(db, district, upazila):
    def _make(donor=True, never=True, last=None, willingness="ACTIVE", blood="O+", active=True, **privacy):
        n = next(_counter)
        user = User.objects.create_user(
            email=f"Member{n}@Example.com", password="Str0ng-pass-phrase!", is_active=active,
        )
        profile = MemberProfile.objects.create(
            user=user, full_name=f"Test Member{n} Khan", phone="01711111111", whatsapp_number="01711111111",
            messenger_url="https://m.me/test", district=district, upazila=upazila, area="Test area",
            wants_to_donate=donor, needs_blood=not donor, blood_group=blood if donor else "",
            never_donated=never if donor else False,
            confirmed_last_donation_date=last, donation_willingness=willingness,
        )
        MemberPrivacy.objects.create(user=user, **privacy)
        return profile

    return _make


@pytest.fixture
def record():
    def _record(profile, days_ago, status=DonationRecord.Status.COMPLETED):
        return DonationRecord.objects.create(
            donor=profile.user, donation_date=timezone.localdate() - timedelta(days=days_ago), status=status
        )

    return _record
