from django.db import models
from PIL import Image
from ckeditor.fields import RichTextField
from django.utils import timezone
# from embed_video.fields import EmbedVideoField
from django.urls import reverse


class Author(models.Model):
    author_name = models.CharField(max_length=40, default="Admin")

    def __str__(self):
        return self.author_name

    class Meta:
        # name the table in db
        db_table = "author"

class Category(models.Model):
    cate_name = models.CharField(max_length=20)

    def __str__(self):
        return self.cate_name

    class Meta:
        # name the table in db
        db_table = "category"
        verbose_name_plural = "categories"
        ordering=["cate_name"]

class Tag(models.Model):
    tag_name = models.CharField(max_length=20)

    def __str__(self):
        return self.tag_name

    class Meta:
        # name the table in db
        db_table = "tag"
        ordering=["tag_name"]

class Max_10_Links(models.Model):
    """add NO more than 10 links!"""
    name = models.CharField(max_length=30)
    href = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = "max_10_links"

class Article(models.Model):
    # the article id will be 4-digit number like 0001 so should be char not integer
    article_id = models.CharField(max_length=4)
    title = models.CharField(max_length=200)
    # preview picture
    preview = models.ImageField(upload_to="article", blank=True, null=True, default=False)
    # preview video # Don't use EmbedVideoField! CharField is better!
    video = models.CharField(blank=True, null=True, default=False, max_length=500)
    # the date will be shown on blog page
    timestamp = models.DateField(default=timezone.now)
    # DateTime only used to sort, not shown on blog page
    time = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING)
    category = models.ManyToManyField(Category)
    tag = models.ManyToManyField(Tag)
    recommend = models.BooleanField(default=False)
    top = models.BooleanField(default=False)
    featured = models.BooleanField(default=True)
    # the overview words will be edited in RichText Editor on admin page
    overview = RichTextField()
    body = models.TextField()
    view_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)

    def remove_on_image_update(self):
        try:
            # is the object in the database yet?
            obj = Article.objects.get(id=self.id)
        except Article.DoesNotExist:
            # object is not in db, nothing to worry about
            return "Article.DoesNotExist"
        # is the save due to an update of the actual image file?
        if obj.preview and self.preview and obj.preview != self.preview:
            # delete the old image file from the storage in favor of the new file
            obj.preview.delete()

    def delete(self, *args, **kwargs):
        # object is being removed from db, remove the file from storage first
        self.preview.delete()
        return super(Article, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # object is possibly being updated, if so, clean up.
        self.remove_on_image_update()
        return super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post:article', args=[str(self.article_id)])

    def viewed(self):
        self.view_count += 1
        self.save(update_fields=["view_count"])

    class Meta:
        # name the table in db
        db_table = "article"
        # multiple ordering priority
        ordering=["-top", "-recommend", "-time"]
        