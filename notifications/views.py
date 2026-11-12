from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from core.permissions import member_required

from . import services


@member_required
def notification_list(request):
    qs = services.with_read_flag(services.visible_for(request.user), request.user)
    page = Paginator(qs, 20).get_page(request.GET.get("page"))
    for item in page:
        item.link = services.target_url(item)
    return render(request, "notifications/list.html", {"page": page})


@member_required
@require_POST
def mark_read(request, pk):
    notification = services.mark_read(request.user, pk)
    return redirect(services.target_url(notification) or "notifications:list")
