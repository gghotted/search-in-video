from django.db import models


class Audio(models.Model):
    file = models.FileField()
    created = models.DateTimeField(auto_now_add=True)


