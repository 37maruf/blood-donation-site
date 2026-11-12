from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from core import throttle
from core.permissions import member_required
from donations.services.eligibility import available_queryset

from .models import ContactAttempt
from .services import allowed_channels, link_for


@member_required
@require_POST
def contact_click(request, donor_id, channel):
    if channel not in ("whatsapp", "messenger"):
        raise Http404
    profile = get_object_or_404(available_queryset(), pk=donor_id)
    if profile.user_id == request.user.pk or channel not in allowed_channels(profile, profile.user.privacy):
        raise Http404
    if not throttle.allow("contact", f"u{request.user.pk}", 20, 3600):
        messages.error(request, "You have used many contact links recently. Please try again later.")
        return redirect("members:donor_detail", profile_id=profile.pk)
    ContactAttempt.objects.create(member=request.user, donor=profile.user, channel=channel.upper())
    return HttpResponseRedirect(link_for(profile, channel))
