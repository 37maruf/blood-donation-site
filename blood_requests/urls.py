from django.urls import path

from . import views

app_name = "blood_requests"
urlpatterns = [
    path("blood-needs/", views.need_list, name="need_list"),
    path("blood-needs/create/", views.need_create, name="need_create"),
    path("blood-needs/mine/", views.need_mine, name="need_mine"),
    path("blood-needs/<uuid:pk>/", views.need_detail, name="need_detail"),
    path("blood-needs/<uuid:pk>/edit/", views.need_edit, name="need_edit"),
    path("blood-needs/<uuid:pk>/close/", views.need_close, name="need_close"),
    path("blood-needs/<uuid:pk>/respond/", views.need_respond, name="need_respond"),
    path("blood-requests/create/", views.general_create, name="general_create"),
    path("blood-requests/mine/", views.general_mine, name="general_mine"),
    path("donors/<uuid:donor_id>/request/", views.request_create, name="request_create"),
    path("donation-requests/sent/", views.request_sent, name="request_sent"),
    path("donation-requests/received/", views.request_received, name="request_received"),
    path("donation-requests/<uuid:pk>/accept/", views.request_accept, name="request_accept"),
    path("donation-requests/<uuid:pk>/reject/", views.request_reject, name="request_reject"),
    path("donation-requests/<uuid:pk>/cancel/", views.request_cancel, name="request_cancel"),
    path("donation-requests/<uuid:pk>/complete/", views.request_complete, name="request_complete"),
]
