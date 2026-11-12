from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from core.exceptions import ServiceError
from core.permissions import member_required

from . import services
from .models import Campaign, CampaignRegistration


def campaign_list(request):
    phase = request.GET.get("when", "upcoming")
    if phase not in ("upcoming", "ongoing", "past", "all"):
        phase = "upcoming"
    qs = services.filter_by_phase(services.public_campaigns(), phase)
    page = Paginator(qs, 9).get_page(request.GET.get("page"))
    tabs = [("upcoming", "Upcoming"), ("ongoing", "Ongoing"), ("past", "Past"), ("all", "All")]
    return render(request, "campaigns/list.html", {"page": page, "phase": phase, "tabs": tabs})


def campaign_detail(request, pk):
    campaign = get_object_or_404(services.public_campaigns(), pk=pk)
    registered = False
    if request.user.is_authenticated:
        registered = campaign.registrations.filter(
            member=request.user, status=CampaignRegistration.Status.REGISTERED).exists()
    taken = campaign.registrations.filter(status=CampaignRegistration.Status.REGISTERED).count()
    return render(request, "campaigns/detail.html", {
        "campaign": campaign, "registered": registered,
        "spots_left": None if campaign.capacity is None else max(campaign.capacity - taken, 0),
    })


@member_required
@require_POST
def campaign_register(request, pk):
    get_object_or_404(services.public_campaigns(), pk=pk)
    try:
        services.register_member(pk, request.user)
        messages.success(request, "You are registered. See you there!")
    except ServiceError as exc:
        messages.error(request, str(exc))
    return redirect("campaigns:detail", pk=pk)
