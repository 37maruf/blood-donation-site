from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET

from .models import SiteContent


def _page(request, key, template="content/page.html", **extra):
    page = get_object_or_404(SiteContent, key=key)
    return render(request, template, {"page": page, **extra})


@require_GET
def about(request):
    return _page(request, "about")


@require_GET
def contact(request):
    return _page(request, "contact", "content/contact.html")


@require_GET
def terms(request):
    return _page(request, "terms")


@require_GET
def privacy(request):
    return _page(request, "privacy", "content/privacy.html")
