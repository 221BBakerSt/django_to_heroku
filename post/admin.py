from django.contrib import admin
from .models import *

class ArticleAdmin(admin.ModelAdmin):

    # choose what to show in article admin page
    list_display = ["title", "id", "article_id", "overview", "top", "recommend", "time", "video"]
    # choose what parameters as filters
    list_filter = ["category", "tag", "recommend", "top"]
    # choose what can be searched in search box
    search_fields = ["article_id", "title", "category", "tag"]
    # filter_horizontal = ["category", "tag"]
    date_hierarchy = "timestamp"
    list_per_page = 20
    actions_on_bottom = True
    # to classify parameters
    fieldsets = (
    ("title & article_id & author", {'fields': (("title", "article_id", "author"),)}),
    ("pic / video", {'fields': (("preview", "video"),)}),
    ("date & time", {'fields': ("timestamp", "time")}),
    ("category & tag", {'fields': ("category", "tag")}),
    ("recommend & top & featured", {'fields': ("recommend", "top", "featured")}),
    ("overview & body", {'fields': ("overview", "body")}),
    ("view & comment & like", {'fields': ("view_count", "comment_count", "like_count")})
    )


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Max_10_Links)
admin.site.register(Article, ArticleAdmin)
