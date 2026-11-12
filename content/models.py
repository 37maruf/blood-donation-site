from django.conf import settings
from django.core.cache import cache
from django.db import models

from django.utils import translation

from core.models import UUIDModel


def _bn_active():
    return (translation.get_language() or "en").startswith("bn")


class SiteContent(UUIDModel):
    key = models.SlugField(unique=True, help_text="Internal key, e.g. about, terms, privacy, home_intro.")
    title = models.CharField(max_length=200)
    body = models.TextField(help_text="Plain text. Blank lines start a new paragraph.")
    title_bn = models.CharField("title (Bangla)", max_length=200, blank=True,
                                help_text="Shown when the visitor picks Bangla. Falls back to English if empty.")
    body_bn = models.TextField("body (Bangla)", blank=True,
                               help_text="Bangla version. Falls back to English if empty.")
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name="+"
    )

    class Meta:
        ordering = ["key"]
        verbose_name = "site content page"

    def __str__(self):
        return self.key

    @property
    def display_title(self):
        return self.title_bn if (_bn_active() and self.title_bn) else self.title

    @property
    def display_body(self):
        return self.body_bn if (_bn_active() and self.body_bn) else self.body


ORG_CACHE_KEY = "org_settings_v1"


class OrganizationSettings(UUIDModel):
    name = models.CharField(max_length=120, default="Surjotori")
    tagline = models.CharField(max_length=160, default="Blood Donation Organization")
    phone = models.CharField(max_length=40, blank=True)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=250, blank=True)
    facebook_url = models.URLField(blank=True)
    messenger_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    retention_note = models.TextField(blank=True, help_text="Data retention periods (shown on the Privacy page).")
    retention_note_bn = models.TextField("retention note (Bangla)", blank=True)

    class Meta:
        verbose_name = "organization settings"
        verbose_name_plural = "organization settings"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(ORG_CACHE_KEY)

    def __str__(self):
        return self.name

    @property
    def display_retention_note(self):
        return self.retention_note_bn if (_bn_active() and self.retention_note_bn) else self.retention_note
