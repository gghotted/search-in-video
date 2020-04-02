from django.db import models
from django.contrib.auth.models import User


class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=100)
    video = models.FileField(null=True)
    audio = models.FileField(null=True)
    source_type = models.CharField(max_length=50)
    youtube_link = models.CharField(max_length=255, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def filter_words(self, startswith):
        return self.words.filter(text__startswith=startswith)

    def script(self):
        return ' '.join(self.words.order_by('start_at').values_list('text', flat=True))

    class Meta:
        ordering = ['-created']


class Word(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='words')
    text = models.CharField(max_length=50)
    start_at = models.TimeField()
    end_at = models.TimeField()

    def __str__(self):
        return self.text

    def near_words(self):
        return Word.objects.filter(start_at__gte=self.start_at).order_by('start_at')[:5]
