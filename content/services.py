from django.core.cache import cache

from .models import ORG_CACHE_KEY, OrganizationSettings


def get_org_settings():
    org = cache.get(ORG_CACHE_KEY)
    if org is None:
        org = OrganizationSettings.objects.first() or OrganizationSettings.objects.create()
        cache.set(ORG_CACHE_KEY, org, 300)
    return org
