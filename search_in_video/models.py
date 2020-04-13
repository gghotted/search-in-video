from django.db import models
from django.contrib.auth.models import User
from django.core.files import File

from .youtube import MyYoutube
from .google_api import recognize_by_google_ocr, get_timestamp_ocr_result
from .google_api import recognize_by_google_stt, get_timestamp_stt_result
from state.consumers import announce

import moviepy.editor as mp
 
 
class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=100)
    video = models.FileField(null=True)
    audio = models.FileField(null=True)
    source_type = models.CharField(max_length=50)
    youtube_link = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title


    def filter_words(self, startswith):
        return self.words.filter(text__startswith=startswith)


    def script(self):
        return ' '.join(self.words.order_by('start_at').values_list('text', flat=True))


    def set_videofile(self, filepath=None, filename=None):
        if filepath:
            self.set_videofile_by_path(filepath, filename)
            return
        
        try:
            yt = MyYoutube(self.youtube_link) 
            filepath = yt.download_best_video(tempfile=True)
            self.set_videofile_by_path(filepath, filename)
        except Exception as e:
            print(e)


    def set_videofile_by_path(self, filepath, filename=None):
        self.video = File(open(filepath, 'rb'))
        self.video.name = filename or (self.title + '.mp4')


    def set_audio(self):
        videofile_path = str(self.video.file)
        mp4 = mp.VideoFileClip(videofile_path)
        mp4.audio.write_audiofile('tmp/tmp.wav')
        audio_file = File(open('tmp/tmp.wav', 'rb'))
        audio_file.name = self.video.name.replace('mp4', 'wav')
        self.audio = audio_file


    def create_words_by_audio(self):
        response = recognize_by_google_stt(self.audio)
        datas = get_timestamp_stt_result(response)
        for text, start_at, end_at in datas:
            Word(video=self,
                 extracted_by='audio',
                 text=text,
                 start_at=start_at,
                 end_at=end_at).save()


    def create_words_by_video(self):
        response = recognize_by_google_ocr(self.video)
        datas = get_timestamp_ocr_result(response)
        for text, start_at, end_at, topleft, bottomright in datas:
            word = Word(video=self,
                        extracted_by='video',
                        text=text,
                        start_at=start_at,
                        end_at=end_at)
            word.save()
            for vertex in [topleft, bottomright]:
                Vertex(word=word,
                       x=vertex.x,
                       y=vertex.y).save()

    
    def synchronize_state(self, state):
        self.state = state
        channel_name = 'state_%s' % self.id
        announce(channel_name, state)
        self.save()

    class Meta:
        ordering = ['-created']


class Word(models.Model):
    video = models.ForeignKey('Video', on_delete=models.CASCADE, related_name='words')
    text = models.CharField(max_length=255)
    extracted_by = models.CharField(max_length=50)
    start_at = models.TimeField()
    end_at = models.TimeField()

    def __str__(self):
        return self.text

    def near_words(self):
        return Word.objects.filter(start_at__gte=self.start_at).order_by('start_at')[:5]


class Vertex(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='vertices')
    x = models.FloatField()
    y = models.FloatField()