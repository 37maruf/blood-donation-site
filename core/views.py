import hmac

from django.conf import settings
from django.db import connection
from django.http import HttpResponseForbidden, JsonResponse
from django.http import Http404
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_GET

from campaigns.services import upcoming_campaigns
from content.models import SiteContent

from . import throttle
from .services import site_stats


@require_GET
def home(request):
    from blood_requests.models import BloodNeedPost

    intro = SiteContent.objects.filter(key="home_intro").first()
    needs = BloodNeedPost.objects.filter(status=BloodNeedPost.Status.ACTIVE, is_hidden=False).order_by("-created_at")[:3]
    return render(
        request,
        "core/home.html",
        {"stats": site_stats(), "campaigns": upcoming_campaigns(3), "intro": intro, "needs": needs},
    )


@require_GET
def health(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return JsonResponse({"status": "ok"})
    except Exception:  # noqa: BLE001 - health must never leak details
        return JsonResponse({"status": "error"}, status=503)


@require_GET
def cron_cleanup(request):
    """Idempotent maintenance job. Vercel Cron sends `Authorization: Bearer $CRON_SECRET`."""
    secret = settings.CRON_SECRET
    supplied = request.headers.get("Authorization", "").removeprefix("Bearer ").strip()
    if not secret or not hmac.compare_digest(secret, supplied):
        return HttpResponseForbidden("Forbidden")
    return JsonResponse({"throttle_rows_deleted": throttle.purge()})


@require_GET
def set_language(request, code):
    """Remember the visitor's language in a cookie and go back to where they were."""
    from .middleware import LANG_COOKIE, SUPPORTED

    if code not in SUPPORTED:
        raise Http404
    target = request.GET.get("next", "/")
    if not url_has_allowed_host_and_scheme(target, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
        target = "/"
    response = redirect(target)
    response.set_cookie(LANG_COOKIE, code, max_age=60 * 60 * 24 * 365, samesite="Lax", secure=request.is_secure())
    return response
