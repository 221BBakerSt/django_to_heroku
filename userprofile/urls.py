from django.urls import re_path
from .views import *

APP_NAME = "userprofile"

urlpatterns = [
    re_path(r"^/?$", profile, name="profile"),
    re_path(r"^/profile$", profile, name="profile"),
]
