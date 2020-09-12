from django.urls import re_path
from django.conf.urls import handler404
from . import views

APP_NAME = "about"
# 经过项目urls的匹配符合条件的被路由到这里，继续匹配。前面已经匹配的部分会被抛弃！
urlpatterns = [
    re_path(r"^/?$", views.about, name="about"),
    re_path(r"^/music?$", views.music, name="music"),
]