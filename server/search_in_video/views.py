from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import View
from django.core.files import File
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import Video, Word
from .util import OverwriteStorage, recognize_by_google_stt, get_timestamp

import moviepy.editor as mp


class IndexView(View):
    def get(self, request):
        videos = None
        if request.user:
            videos = request.user.videos.all()
        return render(request, 'home.html', {'videos': videos})


class ListView(View):
    def get(self, request):
        user = request.user
        find_text = request.GET.get('find_text')

        videos = Video.objects.filter(user=user)
        if find_text:
            videos = videos.filter(words__text__startswith=find_text)

        return render(request, 'list.html', {'videos': videos})


class UploadView(View):
    def get(self, request):
        return render(request, 'upload.html')

    def post(self, request):
        user = request.user
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
        # video = Video(user=user, video=video_file)
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


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('list')
        else:
            error_msg = '잘못된 정보입니다.'
            return render(request, 'login.html', {'error_msg': error_msg})


@login_required
def search(request):
    user = request.user
    find_text = request.GET.get('find_text', '')
    words = Word.objects.filter(video__user=user,
                                text__startswith=find_text)
    response_words = [{'text': word.text,
                       'start_at': word.start_at,
                       'end_at': word.end_at,
                       'video_title': word.video.title,
                       'video_id': word.pk} for word in words]
    return JsonResponse({'words': response_words})


@login_required
def get_video(request, pk):
    video = Video.objects.get(pk=pk)
    response_video = {'url': video.video.url,
                      'title': video.title}
    return JsonResponse({'video': response_video})


