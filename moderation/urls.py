from django.urls import path

from . import views

app_name = "moderation"
urlpatterns = [path("", views.create_report, name="report")]
