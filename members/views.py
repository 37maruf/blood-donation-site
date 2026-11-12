from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET

from contacts.services import allowed_channels
from core.permissions import member_required
from donations.models import DonationRecord
from donations.services.eligibility import DISCLAIMER, available_queryset, evaluate

from . import services
from .forms import DonationSettingsForm, DonorSearchForm, MemberProfileForm, PrivacyForm

PAGE_SIZE = 12


def _page(request, queryset):
    return Paginator(queryset, PAGE_SIZE).get_page(request.GET.get("page"))


@require_GET
def donor_list(request):
    donors = _page(request, services.search_donors())
    return render(request, "members/donor_list.html", {"page": donors, "disclaimer": DISCLAIMER, "search": False})


@require_GET
def donor_search(request):
    form = DonorSearchForm(request.GET or None)
    qs = available_queryset().none()
    searched = bool(request.GET)
    if searched and form.is_valid():
        qs = services.search_donors(
            form.cleaned_data["blood_group"], form.cleaned_data["upazila"], form.cleaned_data["area"]
        )
    elif not searched:
        qs = services.search_donors()
    page = _page(request, qs)
    query = request.GET.copy()
    query.pop("page", None)
    return render(request, "members/donor_list.html", {
        "page": page, "form": form, "disclaimer": DISCLAIMER, "search": True, "querystring": query.urlencode(),
    })


@member_required
def donor_detail(request, profile_id):
    profile = get_object_or_404(available_queryset(), pk=profile_id)
    if profile.user_id == request.user.pk:
        return redirect("members:profile")
    privacy = profile.user.privacy
    history = []
    if privacy.show_donation_history:
        history = list(DonationRecord.objects.filter(
            donor=profile.user, status=DonationRecord.Status.COMPLETED).order_by("-donation_date")[:20])
    return render(request, "members/donor_detail.html", {
        "profile": profile, "privacy": privacy, "history": history,
        "channels": allowed_channels(profile, privacy), "disclaimer": DISCLAIMER,
        "can_request": privacy.allow_direct_requests,
    })


@member_required
def profile_detail(request):
    profile = request.user.profile
    return render(request, "members/profile.html", {
        "profile": profile, "privacy": request.user.privacy, "eligibility": evaluate(profile), "disclaimer": DISCLAIMER,
    })


@member_required
def profile_edit(request):
    profile = request.user.profile
    form = MemberProfileForm(request.POST or None, request.FILES or None, instance=profile)
    if request.method == "POST" and form.is_valid():
        services.save_profile(request, form)
        messages.success(request, "Profile updated.")
        return redirect("members:profile")
    return render(request, "generic_form.html", {
        "form": form, "title": "Edit profile", "submit_label": "Save changes", "multipart": True,
        "back_url": "members:profile",
    })


@member_required
def privacy_settings(request):
    privacy = request.user.privacy
    old = privacy.snapshot()
    form = PrivacyForm(request.POST or None, instance=privacy)
    if request.method == "POST" and form.is_valid():
        services.update_privacy(request, form, old)
        messages.success(request, "Contact & privacy settings saved.")
        return redirect("members:privacy_settings")
    return render(request, "generic_form.html", {
        "form": form, "title": "Contact & privacy", "submit_label": "Save settings", "back_url": "members:profile",
        "intro": "Everything is OFF by default. Only what you switch on is shown, and only to logged-in members.",
    })


@member_required
def donation_settings(request):
    profile = request.user.profile
    if not profile.wants_to_donate:
        messages.info(request, "Turn on 'I want to donate' in your profile first.")
        return redirect("members:profile_edit")
    form = DonationSettingsForm(request.POST or None, profile=profile)
    if request.method == "POST" and form.is_valid():
        services.update_donation_settings(request, profile, form.cleaned_data)
        messages.success(request, "Donation settings saved.")
        return redirect("members:profile")
    return render(request, "generic_form.html", {
        "form": form, "title": "Donation willingness", "submit_label": "Save", "back_url": "members:profile",
        "intro": "Inactive members are removed from donor lists. When reactivating, confirm your last donation.",
        "disclaimer": DISCLAIMER,
    })
