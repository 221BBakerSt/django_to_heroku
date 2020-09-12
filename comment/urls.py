from django.urls import path, re_path
from . import views

APP_NAME = "comment"

urlpatterns = [
    path("post/<int:article_id>/", views.post_comment, name="post_comment"),
    re_path("delete/(\d+)/(\d+)/", views.delete_comment, name="delete_comment"),
]