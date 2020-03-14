from django.shortcuts import render, HttpResponse
from django.views import generic
from .models import Video, Word
from .util import OverwriteStorage, recognize_by_google_stt, get_timestamp
from django.core.files import File
import moviepy.editor as mp


class IndexView(generic.View):
    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        video_file = request.FILES['file']
        file_name = video_file.name[:-4]

        # # mp4로 로컬에 save
        # fs = OverwriteStorage(location='tmp/')
        # fs.save('tmp.mp4', video_file)
        #
        # # mp4 to wav
        # clip = mp.VideoFileClip('tmp/tmp.mp4')
        # clip.audio.write_audiofile('tmp/tmp.wav')
        # audio_file = File(open('tmp/tmp.wav', 'rb'))
        #
        # # db, cloud 저장소에 save
        # video = Video(video=video_file)
        # video.audio.save(file_name+'.wav', audio_file)
        # video.save()
        #
        # response = recognize_by_google_stt(str(video.audio))
        #
        # # 인식된 word 를 db에 저장
        # for text, start_at, end_at in get_timestamp(response):
        #     Word(text=text, start_at=start_at, end_at=end_at,
        #          video=video).save()
        #     print(text, start_at, end_at, '저장완료')

        return HttpResponse('완료')

