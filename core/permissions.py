from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def member_required(view):
    """Logged-in user that has a member profile."""

    @login_required
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, "profile"):
            messages.warning(request, "This account has no member profile.")
            return redirect("core:home")
        return view(request, *args, **kwargs)

    return wrapper

