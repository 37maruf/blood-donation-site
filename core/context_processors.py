from django.conf import settings

from content.services import get_org_settings


def site(request):
    lang = getattr(request, "LANGUAGE_CODE", "en")
    ctx = {
        "org": get_org_settings(), "TERMS_VERSION": settings.TERMS_VERSION,
        "LANG": lang, "IS_BN": lang == "bn", "OTHER_LANG": "en" if lang == "bn" else "bn",
    }
    user = getattr(request, "user", None)
    if user is not None and user.is_authenticated:
        from notifications.services import unread_count

        ctx["unread_count"] = unread_count(user)
    return ctx
