from django.db import models
from django.contrib.auth.models import User


class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    video = models.FileField()
    audio = models.FileField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def filter_words(self, startswith):
        return self.words.filter(text__startswith=startswith)


class Word(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='words')
    text = models.CharField(max_length=50)
    start_at = models.TimeField()
    end_at = models.TimeField()
