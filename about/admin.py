from django.contrib import admin
from .models import *

class BoardAdmin(admin.ModelAdmin):
    list_display = ["id", "nickname", "email", "subject", "message", "timestamp"]
    list_filter = ["email"]
    search_fields = ["nickname", "email", "subject"]
    list_per_page = 20
    actions_on_bottom = True

class BulletinAdmin(admin.ModelAdmin):
    list_display = ["title", "body"]

class SongAdmin(admin.ModelAdmin):
    list_display = ["name", "artist", "audio_file"]


admin.site.register(Board, BoardAdmin)
admin.site.register(Owner)
admin.site.register(Bulletin, BulletinAdmin)
admin.site.register(Song, SongAdmin)
