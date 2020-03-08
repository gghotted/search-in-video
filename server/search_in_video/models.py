from django.db import models


class Video(models.Model):
    video = models.FileField()
    audio = models.FileField()
    created = models.DateTimeField(auto_now_add=True)
