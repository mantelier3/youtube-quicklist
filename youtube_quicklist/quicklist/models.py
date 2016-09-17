from __future__ import unicode_literals

from django.db import models

# Create your models here.

class User(models.Model):
    session_id = models.CharField(max_length=120)

class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    playlist_name = models.CharField(max_length=20)
    # @classmethod
    # def create(cls, name, email):
    #     return cls(name=name, email=email)

class Results(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    results_name = models.CharField(max_length=20)

class Video(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, blank=True, null=True)
    results = models.ForeignKey(Results, on_delete=models.CASCADE, blank=True, null=True)
    video_id = models.CharField(max_length=20)
    thumbnail_url = models.CharField(max_length=120)
    # video_url = models.CharField(max_length=120)
