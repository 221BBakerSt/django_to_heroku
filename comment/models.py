from django.db import models
from post.models import *
from django.conf import settings
User = settings.AUTH_USER_MODEL
from ckeditor.fields import RichTextField


class Comment(models.Model):
    
    article = models.ForeignKey(Article, on_delete=models.DO_NOTHING, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="comments")
    body = RichTextField()
    comment_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("comment_time",)

    def __str__(self):
        return self.body[:20]