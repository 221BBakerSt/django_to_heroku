from django.urls import path, re_path
from . import views

APP_NAME = "post"

urlpatterns = [
    re_path(r"^/?$", views.post, name="post"),
    re_path(r"^/([0-9]{4})/?$", views.article, name="article"),
    re_path(r"^/search", views.search, name="search"),
    re_path(r"^/author/(\w+)/?$", views.author_filter, name="author_filter"),
    re_path(r"^/category/(\w+)/?$", views.category_filter, name="category_filter"),
    re_path(r"^/tag/(\w+)/?$", views.tag_filter, name="tag_filter"),
]
