from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("", include("content.urls")),
    path("accounts/", include("accounts.urls")),
    path("campaigns/", include("campaigns.urls")),
    path("", include("members.urls")),
    path("", include("contacts.urls")),
    path("", include("blood_requests.urls")),
    path("dashboard/notifications/", include("notifications.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("report/", include("moderation.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = "config.views.error_403"
handler404 = "config.views.error_404"
handler500 = "config.views.error_500"
