from django.contrib import admin
from .models import *


class CommentAdmin(admin.ModelAdmin):
    # choose what to show in article admin page
    list_display = ["user", "comment_time", "body"]
    # choose what parameters as filters
    list_filter = ["user", "comment_time"]
    # choose what can be searched in search box
    search_fields = ["user", "body"]
    date_hierarchy = "comment_time"
    list_per_page = 20
    actions_on_bottom = True

admin.site.register(Comment, CommentAdmin)