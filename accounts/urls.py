from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views

app_name = "accounts"
urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.ThrottledLoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("security/", views.security, name="security"),
    path("password-reset/", views.ThrottledPasswordResetView.as_view(), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(
        template_name="message.html",
        extra_context={"title": "Check your email", "message": "If an account exists for that address, reset instructions are on their way."},
    ), name="password_reset_done"),
    path("password-reset/<uidb64>/<token>/", views.ConfirmView.as_view(), name="password_reset_confirm"),
    path("password-reset/complete/", auth_views.PasswordResetCompleteView.as_view(
        template_name="message.html",
        extra_context={"title": "Password changed", "message": "You can now log in with your new password."},
    ), name="password_reset_complete"),
]
