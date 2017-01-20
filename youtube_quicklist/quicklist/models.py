from __future__ import unicode_literals
from django.db import models


class User(models.Model):
    session_id = models.CharField(max_length=120)


class Playlist(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Video(models.Model):
    video_id = models.CharField(max_length=20)
    thumbnail_url = models.CharField(max_length=120)
    playlists = models.ManyToManyField(Playlist)

    def __str__(self):
        return self.video_id


class Results(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,
                             null=True)
    results_name = models.CharField(max_length=20)
