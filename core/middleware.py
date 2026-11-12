"""Language selection (English / Bangla) stored in a cookie.

The active language drives Django's own translated strings (validation errors, month names)
and the project's templates via the `bilingual` template library.
"""
from django.utils import translation
from django.utils.cache import patch_vary_headers

LANG_COOKIE = "lang"
SUPPORTED = ("en", "bn")


def pick_language(request):
    chosen = request.COOKIES.get(LANG_COOKIE)
    if chosen in SUPPORTED:
        return chosen
    # First visit: follow the browser if it prefers Bangla.
    header = request.META.get("HTTP_ACCEPT_LANGUAGE", "").lower()
    first = header.split(",")[0].strip() if header else ""
    return "bn" if first.startswith("bn") else "en"


class LanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        lang = pick_language(request)
        translation.activate(lang)
        request.LANGUAGE_CODE = lang
        try:
            response = self.get_response(request)
        finally:
            translation.deactivate()
        response.headers.setdefault("Content-Language", lang)
        patch_vary_headers(response, ("Cookie",))
        return response
