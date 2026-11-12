from django.contrib import messages
from django.shortcuts import redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from core import throttle
from core.permissions import member_required

from .forms import ReportForm
from .models import Report
from .services import audit


@member_required
@require_POST
def create_report(request):
    back = request.META.get("HTTP_REFERER", "")
    if not url_has_allowed_host_and_scheme(back, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
        back = "/"
    if not throttle.allow("report", f"u{request.user.pk}", 10, 3600):
        messages.error(request, "You are sending reports too quickly. Please try again later.")
        return redirect(back)
    form = ReportForm(request.POST, reporter=request.user)
    if form.is_valid():
        report = Report.objects.create(reporter=request.user, **form.cleaned_data)
        audit(request.user, "report.created", report.target_type, report.target_id, request=request)
        messages.success(request, "Thank you. Our team will review your report.")
    else:
        messages.error(request, "The report could not be submitted. Please check the details and try again.")
    return redirect(back)
