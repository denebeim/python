from django.urls import path

from accounts.views import send_login_email, login


urlpatterns = [
    path(
        "send_login_email",
        send_login_email,
        name="send_login_email",
    ),
    path(
        "login",
        login,
        name="login",
    ),
]
