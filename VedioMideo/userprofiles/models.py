from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
import datetime

# Create your models here.
class New(models.Model):
    alert = models.CharField(max_length=45)
    sumary = models.CharField(max_length= 45)
    date = models.DateTimeField(auto_now_add=True)
    id_user = models.ForeignKey(User)

    def __str__(self):
        return self.alert

class Video(models.Model):
    title = models.CharField(max_length=45)
    sumary = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    searched = models.IntegerField(default=0)
    id_user = models.ForeignKey(User)
    video = models.FileField(upload_to="videos/%Y/%m/", blank=False)
    thumbnail = models.ImageField(upload_to='img/%Y/%m/', default='img/default.png')

    def __str__(self):
        return self.title