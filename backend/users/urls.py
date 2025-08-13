from django.urls import path
from .views import signup_request, verification, login, who_am_i

urlpatterns = [
    path("signup/",signup_request),
    path("verification/", verification),
    path("login/", login),
    path("who_am_i/",who_am_i),
]