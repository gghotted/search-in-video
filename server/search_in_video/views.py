from django.shortcuts import render, HttpResponse
from django.views import generic
from .models import Video
from .util import OverwriteStorage
from django.core.files import File
import moviepy.editor as mp


class IndexView(generic.View):
    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        video_file = request.FILES['file']
        file_name = video_file.name[:-4]

        # mp4로 로컬에 save
        fs = OverwriteStorage(location='tmp/')
        fs.save('tmp.mp4', video_file)

        # mp4 to wav
        clip = mp.VideoFileClip('tmp/tmp.mp4')
        clip.audio.write_audiofile('tmp/tmp.wav')
        audio_file = File(open('tmp/tmp.wav', 'rb'))

        # db, cloud 저장소에 save
        video = Video(video=video_file)
        video.audio.save(file_name+'.wav', audio_file)
        video.save()

        return HttpResponse('완료')

