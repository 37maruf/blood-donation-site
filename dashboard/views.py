from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

from blood_requests.models import BloodNeedPost, DonationRequest, GeneralBloodRequest
from core.permissions import member_required
from core.services import site_stats
from donations.models import DonationRecord
from donations.services.eligibility import DISCLAIMER, evaluate
from notifications.services import unread_count


@member_required
def index(request):
    user = request.user
    P = DonationRequest.Status
    counts = {  # always scoped to request.user
        "unread": unread_count(user),
        "donations": DonationRecord.objects.filter(donor=user).count(),
        "needs": BloodNeedPost.objects.filter(owner=user).count(),
        "general": GeneralBloodRequest.objects.filter(requester=user).count(),
        "received": DonationRequest.objects.filter(donor=user, status=P.PENDING).count(),
        "sent": DonationRequest.objects.filter(requester=user).count(),
    }
    profile = user.profile
    return render(request, "dashboard/index.html", {
        "counts": counts, "profile": profile, "eligibility": evaluate(profile) if profile.wants_to_donate else None,
        "disclaimer": DISCLAIMER,
    })


@member_required
def donation_history(request):
    records = DonationRecord.objects.filter(donor=request.user)
    return render(request, "dashboard/donations.html", {"records": records})


@staff_member_required
def staff_stats(request):
    return render(request, "dashboard/staff_stats.html", {
        "stats": site_stats(),
        "open_general": GeneralBloodRequest.objects.exclude(
            status__in=[GeneralBloodRequest.Status.FULFILLED, GeneralBloodRequest.Status.CANCELLED]).count(),
    })
