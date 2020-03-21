from django.db import models
from django.contrib.auth.models import User


class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.FileField()
    audio = models.FileField()
    created = models.DateTimeField(auto_now_add=True)

class Word(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='words')
    text = models.CharField(max_length=50)
    start_at = models.TimeField()
    end_at = models.TimeField()
