from collections import Counter

from django.core.cache import cache

STATS_KEY = "site_stats_v2"


def site_stats():
    """Counts only, no PII. Cached for 5 minutes."""
    stats = cache.get(STATS_KEY)
    if stats is None:
        from accounts.models import User
        from blood_requests.models import BloodNeedPost
        from core.choices import BloodGroup
        from donations.models import DonationRecord
        from donations.services.eligibility import available_queryset

        # counted in Python on purpose: the eligibility queryset carries annotations that would
        # change a GROUP BY, and the number of available donors in one district is small.
        per_group = Counter(available_queryset().order_by().values_list("blood_group", flat=True))
        stats = {
            # one entry per blood group, in display order (counts only, no personal data)
            "by_group": [{"group": value, "count": per_group.get(value, 0)} for value, _label in BloodGroup.choices],
            "members": User.objects.filter(is_active=True, profile__isnull=False).count(),
            "available_donors": available_queryset().count(),
            "completed_donations": DonationRecord.objects.filter(status=DonationRecord.Status.COMPLETED).count(),
            "active_needs": BloodNeedPost.objects.filter(
                status=BloodNeedPost.Status.ACTIVE, is_hidden=False
            ).count(),
        }
        cache.set(STATS_KEY, stats, 300)
    return stats
