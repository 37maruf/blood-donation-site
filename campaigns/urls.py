from django.urls import path

from . import views

app_name = "campaigns"
urlpatterns = [
    path("", views.campaign_list, name="list"),
    path("<uuid:pk>/", views.campaign_detail, name="detail"),
    path("<uuid:pk>/register/", views.campaign_register, name="register"),
]
