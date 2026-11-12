from django.urls import path

from . import views

app_name = "members"
urlpatterns = [
    path("donors/", views.donor_list, name="donor_list"),
    path("donors/search/", views.donor_search, name="donor_search"),
    path("donors/<uuid:profile_id>/", views.donor_detail, name="donor_detail"),
    path("profile/", views.profile_detail, name="profile"),
    path("profile/edit/", views.profile_edit, name="profile_edit"),
    path("profile/privacy/", views.privacy_settings, name="privacy_settings"),
    path("profile/donation-settings/", views.donation_settings, name="donation_settings"),
]
