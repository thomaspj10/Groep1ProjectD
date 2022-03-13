from django.conf import settings
from django.db import models
from django.utils import timezone
# A post class, can be used to publish blog posts. (From a tutorial :P)

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Album(models.Model):
    artist = models.CharField(max_length = 250)
    album_title = models.CharField(max_length = 250)
    album_logo = models.CharField(max_length = 1000)

    def __str__(self):
        return self.album_title + ' - ' + self.artist


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    file_type = models.CharField(max_length=10)
    song_title = models.CharField(max_length=250)
    genre = models.CharField(max_length=250)

    def __str__(self):
        return self.song_title