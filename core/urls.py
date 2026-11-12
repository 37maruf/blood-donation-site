from django.urls import path

from . import views

app_name = "core"
urlpatterns = [
    path("", views.home, name="home"),
    path("health/", views.health, name="health"),
    path("lang/<str:code>/", views.set_language, name="set_language"),
    path("internal/cron/cleanup/", views.cron_cleanup, name="cron_cleanup"),
]
