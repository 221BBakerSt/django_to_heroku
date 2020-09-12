from django.urls import re_path
from django.conf.urls import handler404
from . import views

APP_NAME = "album"

urlpatterns = [
    re_path(r"^/?$", views.album, name="album"),
    re_path(r"^/(\w+)/?$", views.gallery, name="gallery"),
]
