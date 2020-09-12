from django.contrib import admin
from .models import *

class SlideAdmin(admin.ModelAdmin):
    # choose what to show in article admin page
    list_display = ["description", "slide_pic"]


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1

class PhotoAdmin(admin.ModelAdmin):
    # choose what to show in article admin page
    list_display = ["description", "gallery", "photo_pic", "time"]
    # choose what parameters as filters
    list_filter = ["gallery"]
    # choose what can be searched in search box
    search_fields = ["gallery"]
    date_hierarchy = "time"
    list_per_page = 20
    actions_on_bottom = True

class GalleryAdmin(admin.ModelAdmin):
    # choose what to show in article admin page
    list_display = ["name", "description", "cover", "timestamp"]
    # choose what parameters as filters
    list_filter = ["name"]
    date_hierarchy = "timestamp"
    list_per_page = 20
    actions_on_bottom = True
    inlines = [PhotoInline]

admin.site.register(Slide, SlideAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Photo, PhotoAdmin)
