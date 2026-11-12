from django.urls import path

from . import views

app_name = "contacts"
urlpatterns = [
    path("donors/<uuid:donor_id>/contact/<str:channel>/", views.contact_click, name="click"),
]
