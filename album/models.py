from django.db import models
from PIL import Image
from django.utils import timezone

class Slide(models.Model):

    description = models.CharField(max_length=100, blank=True, null=True)
    slide_pic = models.ImageField(upload_to="slide", blank=True, null=True, default=False)
    def remove_on_image_update(self):
        try:
            # is the object in the database yet?
            obj = Slide.objects.get(id=self.id)
        except Slide.DoesNotExist:
            # object is not in db, nothing to worry about
            return "Slide.DoesNotExist"
        # is the save due to an update of the actual image file?
        if obj.slide_pic and self.slide_pic and obj.slide_pic != self.slide_pic:
            # delete the old image file from the storage in favor of the new file
            obj.slide_pic.delete()

    def delete(self, *args, **kwargs):
        # object is being removed from db, remove the file from storage first
        self.slide_pic.delete()
        return super(Slide, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # object is possibly being updated, if so, clean up.
        self.remove_on_image_update()
        return super(Slide, self).save(*args, **kwargs)

    def __str__(self):
        return self.description

    class Meta:
        # name the table in db
        db_table = "slide"


class Gallery(models.Model):

    cover = models.ImageField(upload_to="gallery", blank=True, null=True, default=False)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True, null=True)
    # the date will be shown on blog page
    timestamp = models.DateField(default=timezone.now)

    def remove_on_image_update(self):
        try:
            # is the object in the database yet?
            obj = Gallery.objects.get(id=self.id)
        except Gallery.DoesNotExist:
            # object is not in db, nothing to worry about
            return "Gallery.DoesNotExist"
        # is the save due to an update of the actual image file?
        if obj.cover and self.cover and obj.cover != self.cover:
            # delete the old image file from the storage in favor of the new file
            obj.cover.delete()

    def delete(self, *args, **kwargs):
        # object is being removed from db, remove the file from storage first
        self.cover.delete()
        return super(Gallery, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # object is possibly being updated, if so, clean up.
        self.remove_on_image_update()
        return super(Gallery, self).save(*args, **kwargs)


    def __str__(self):
        return self.name

    class Meta:
        # name the table in db
        db_table = "gallery"
        verbose_name_plural = "galleries"
        ordering=["timestamp", "name"]
    
    
class Photo(models.Model):

    photo_pic = models.ImageField(upload_to="photo", blank=True, null=True, default=False)
    description = models.CharField(max_length=200, blank=True, null=True)
    gallery = models.ForeignKey(Gallery, on_delete=models.DO_NOTHING)
    # the date will be shown on blog page
    timestamp = models.DateField(default=timezone.now)
    # DateTime only used to sort, not shown on blog page
    time = models.DateTimeField(default=timezone.now)
    view_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    
    def remove_on_image_update(self):
        try:
            # is the object in the database yet?
            obj = Photo.objects.get(id=self.id)
        except Photo.DoesNotExist:
            # object is not in db, nothing to worry about
            return "Photo.DoesNotExist"
        # is the save due to an update of the actual image file?
        if obj.photo_pic and self.photo_pic and obj.photo_pic != self.photo_pic:
            # delete the old image file from the storage in favor of the new file
            obj.photo_pic.delete()

    def delete(self, *args, **kwargs):
        # object is being removed from db, remove the file from storage first
        self.photo_pic.delete()
        return super(Photo, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # object is possibly being updated, if so, clean up.
        self.remove_on_image_update()
        return super(Photo, self).save(*args, **kwargs)

    def __str__(self):
        if self.description:
            return self.description
        else:
            return "untitled"

    class Meta:
        # name the table in db
        db_table = "photo"
        ordering=["time"]
