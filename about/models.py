from django.db import models
from PIL import Image


class Board(models.Model):
    # 4 blanks for the guest to fill
    nickname = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    subject = models.CharField(max_length=512, blank=True)
    message = models.TextField(max_length=2000, blank=True)
    # record the time and the date of the message
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

    class Meta:
        # name the table in db
        db_table = "guest_board"


class Owner(models.Model):
    pic = models.ImageField(upload_to="owner", blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def remove_on_image_update(self):
        try:
            # is the object in the database yet?
            obj = Owner.objects.get(id=self.id)
        except Owner.DoesNotExist:
            # object is not in db, nothing to worry about
            return "Owner.DoesNotExist"
        # is the save due to an update of the actual image file?
        if obj.pic and self.pic and obj.pic != self.pic:
            # delete the old image file from the storage in favor of the new file
            obj.pic.delete()

    def delete(self, *args, **kwargs):
        # object is being removed from db, remove the file from storage first
        self.pic.delete()
        return super(Owner, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # object is possibly being updated, if so, clean up.
        self.remove_on_image_update()
        return super(Owner, self).save(*args, **kwargs)

    def __str__(self):
        return self.description[:40]


class Bulletin(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class Song(models.Model):
    name = models.CharField(max_length=200)
    artist = models.CharField(max_length=100)
    audio_file = models.FileField(upload_to="music")

    def remove_on_image_update(self):
        try:
            # is the object in the database yet?
            obj = Song.objects.get(id=self.id)
        except Song.DoesNotExist:
            # object is not in db, nothing to worry about
            return "Song.DoesNotExist"
        # is the save due to an update of the actual image file?
        if obj.audio_file and self.audio_file and obj.audio_file != self.audio_file:
            # delete the old image file from the storage in favor of the new file
            obj.audio_file.delete()

    def delete(self, *args, **kwargs):
        # object is being removed from db, remove the file from storage first
        self.audio_file.delete()
        return super(Song, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # object is possibly being updated, if so, clean up.
        self.remove_on_image_update()
        return super(Song, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "song"


