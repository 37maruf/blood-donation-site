from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from core.exceptions import ServiceError
from core.permissions import member_required
from donations.services.eligibility import DISCLAIMER, available_queryset
from moderation.models import Report

from . import services
from .forms import (
    BloodNeedForm,
    DirectRequestForm,
    GeneralBloodRequestForm,
    NeedFilterForm,
    NeedResponseForm,
)
from .models import BloodNeedPost, DonationRequest, GeneralBloodRequest

PAGE_SIZE = 12


# ------------------------------------------------------------------ Blood needs
def need_list(request):
    form = NeedFilterForm(request.GET or None)
    qs = BloodNeedPost.objects.filter(is_hidden=False)
    status = "ACTIVE"
    if form.is_valid():
        status = form.cleaned_data.get("status") or "ACTIVE"
        if form.cleaned_data.get("blood_group"):
            qs = qs.filter(blood_group=form.cleaned_data["blood_group"])
    if status != "ALL":
        qs = qs.filter(status=status)
    qs = qs.order_by("required_date", "-created_at")
    query = request.GET.copy()
    query.pop("page", None)
    page = Paginator(qs, PAGE_SIZE).get_page(request.GET.get("page"))
    return render(request, "blood_requests/need_list.html", {"page": page, "form": form, "querystring": query.urlencode()})


def need_detail(request, pk):
    qs = BloodNeedPost.objects.all()
    post = get_object_or_404(qs, pk=pk)
    is_owner = request.user.is_authenticated and post.owner_id == request.user.pk
    if post.is_hidden and not is_owner:
        return render(request, "404.html", status=404)
    show_contact = request.user.is_authenticated and post.contact_public
    return render(request, "blood_requests/need_detail.html", {
        "post": post, "is_owner": is_owner, "show_contact": show_contact,
        "response_form": NeedResponseForm(), "report_type": Report.TargetType.POST,
    })


@member_required
def need_create(request):
    form = BloodNeedForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        try:
            post = services.create_need_post(request.user, form)
        except ServiceError as exc:
            messages.error(request, str(exc))
        else:
            messages.success(request, "Your blood need is now public and members were notified.")
            return redirect("blood_requests:need_detail", pk=post.pk)
    return render(request, "generic_form.html", {
        "form": form, "title": "Post a blood need", "submit_label": "Publish request",
        "intro": "This post is PUBLIC. Patient name and contact stay hidden unless you tick the options.",
    })


@member_required
def need_mine(request):
    posts = BloodNeedPost.objects.filter(owner=request.user)
    return render(request, "blood_requests/need_mine.html", {"posts": posts})


@member_required
def need_edit(request, pk):
    post = get_object_or_404(BloodNeedPost, pk=pk, owner=request.user)
    if post.status != BloodNeedPost.Status.ACTIVE:
        messages.info(request, "Closed posts cannot be edited.")
        return redirect("blood_requests:need_detail", pk=post.pk)
    form = BloodNeedForm(request.POST or None, instance=post)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Post updated.")
        return redirect("blood_requests:need_detail", pk=post.pk)
    return render(request, "generic_form.html", {
        "form": form, "title": "Edit blood need", "submit_label": "Save changes",
        "back_url": "blood_requests:need_mine",
    })


@member_required
@require_POST
def need_close(request, pk):
    post = get_object_or_404(BloodNeedPost, pk=pk, owner=request.user)
    try:
        services.close_need_post(post, request.user, request.POST.get("status", ""))
        messages.success(request, "Post closed.")
    except ServiceError as exc:
        messages.error(request, str(exc))
    return redirect("blood_requests:need_detail", pk=post.pk)


@member_required
@require_POST
def need_respond(request, pk):
    post = get_object_or_404(BloodNeedPost, pk=pk, is_hidden=False)
    form = NeedResponseForm(request.POST)
    message = form.cleaned_data.get("message", "") if form.is_valid() else ""
    try:
        services.respond_to_need(post, request.user, message)
        messages.success(request, "Thank you! The owner has been notified.")
    except ServiceError as exc:
        messages.error(request, str(exc))
    return redirect("blood_requests:need_detail", pk=post.pk)


# ------------------------------------------------------------------ General requests (private)
@member_required
def general_create(request):
    form = GeneralBloodRequestForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        try:
            services.create_general_request(request.user, form)
        except ServiceError as exc:
            messages.error(request, str(exc))
        else:
            messages.success(request, "Request submitted. Our team will review it; it is not made public.")
            return redirect("blood_requests:general_mine")
    return render(request, "generic_form.html", {
        "form": form, "title": "Request blood (private)", "submit_label": "Submit for review",
        "intro": "Only you and our review team can see this. We will contact you; nothing is published automatically.",
    })


@member_required
def general_mine(request):
    return render(request, "blood_requests/general_mine.html", {
        "requests": GeneralBloodRequest.objects.filter(requester=request.user)})


# ------------------------------------------------------------------ Direct requests (private)
@member_required
def request_create(request, donor_id):
    profile = get_object_or_404(available_queryset(), pk=donor_id)
    if profile.user_id == request.user.pk:
        return redirect("members:profile")
    if not profile.user.privacy.allow_direct_requests:
        messages.info(request, "This donor is not accepting direct requests.")
        return redirect("members:donor_detail", profile_id=profile.pk)
    form = DirectRequestForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        try:
            services.create_direct_request(request.user, profile, form, request)
        except ServiceError as exc:
            messages.error(request, str(exc))
        else:
            messages.success(request, "Request sent. The donor has been notified.")
            return redirect("blood_requests:request_sent")
    return render(request, "generic_form.html", {
        "form": form, "title": f"Request {profile.blood_group} blood from {profile.masked_name}",
        "title_bn": f"{profile.masked_name}-এর কাছে {profile.blood_group} রক্তের অনুরোধ",
        "submit_label": "Send request", "disclaimer": DISCLAIMER,
        "back_url": None, "intro": "Your request is private to this donor. The donor may accept or decline.",
    })


@member_required
def request_sent(request):
    qs = DonationRequest.objects.filter(requester=request.user).select_related("donor__profile")
    return render(request, "blood_requests/requests_list.html", {"requests": qs, "mode": "sent"})


@member_required
def request_received(request):
    qs = DonationRequest.objects.filter(donor=request.user).select_related("requester__profile")
    return render(request, "blood_requests/requests_list.html", {"requests": qs, "mode": "received"})


def _transition(action):
    @member_required
    @require_POST
    def view(request, pk):
        try:
            services.transition_direct_request(pk, request.user, action, request)
            messages.success(request, "Request updated.")
        except ServiceError as exc:
            messages.error(request, str(exc))
        return redirect(request.POST.get("back") == "sent" and "blood_requests:request_sent" or "blood_requests:request_received")

    view.__name__ = f"request_{action}"
    return view


request_accept = _transition("accept")
request_reject = _transition("reject")
request_cancel = _transition("cancel")
request_complete = _transition("complete")
