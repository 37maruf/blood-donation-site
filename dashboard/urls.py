from django.urls import path

from . import views

app_name = "dashboard"
urlpatterns = [
    path("", views.index, name="index"),
    path("donations/", views.donation_history, name="donations"),
    path("staff/", views.staff_stats, name="staff_stats"),
]
