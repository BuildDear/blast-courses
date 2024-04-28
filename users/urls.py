
from django.urls import path

from users.endpoint.google import google_views

urlpatterns = [
    path("", google_views.google_login, name="google-login"),
    path("google/", google_views.google_auth),
]
