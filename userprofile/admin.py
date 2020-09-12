from django.contrib import admin
from .models import *


class UserAdmin(admin.ModelAdmin):
    # choose what to show in article admin page
    list_display = ["username", "id", "email", "date_joined", "last_login"]
    # choose what parameters as filters
    list_filter = ["is_superuser", "is_staff", "is_active"]
    # choose what can be searched in search box
    search_fields = ["username", "id", "email"]
    # filter_horizontal = ["category", "tag"]
    ordering = ["-date_joined", "username"]
    list_per_page = 20
    actions_on_bottom = True

admin.site.register(User, UserAdmin)
