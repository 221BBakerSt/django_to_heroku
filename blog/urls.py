from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url, handler400, handler403, handler404, handler500
from .views import *
from userprofile import views
from django.conf import settings
from django.conf.urls.static import static
# load static files during production
from django.views.static import serve


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index),
    path("blog", include(("post.urls", "post"), namespace="post")),
    path("album", include(("album.urls", "album"), namespace="album")),
    path("about", include(("about.urls", "about"), namespace="about")),
    path("comment", include(("comment.urls", "comment"), namespace="comment")),
    # django-allauth lib
    url(r"^accounts/", include("allauth.urls")),
    # userprofile app to consummate django-allauth
    url(r"^accounts", include(("userprofile.urls", "userprofile"), namespace="userprofile")),
    # django-markdownx lib
    url(r"^markdownx", include("markdownx.urls")),
    # load static files during production
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}, name='static'),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = bad_request
handler403 = permission_denied
handler404 = page_not_found
handler500 = server_error
