from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import View
from django.core.files import File
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import Video, Word
from .util import OverwriteStorage, recognize_by_google_stt, get_timestamp, youtube_download

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
            videos = videos.filter(words__text__startswith=find_text).order_by('-created').distinct()

        return render(request, 'list.html', {'videos': videos})


class UploadView(View):
    def get(self, request, method='choice'):
        template_name = 'upload_' + method.replace('-', '_') + '.html'
        return render(request, template_name)

    def post(self, request, method):
        # mp4, wav save on db
        video = Video()
        video.user = request.user
        video.title = request.POST['title']

        # video_file 할당
        if method == 'mypc':
            video_file = request.FILES['file']
            OverwriteStorage('tmp/').save('tmp.mp4', video_file)
        else:
            video_file = youtube_download(request.POST['youtube_link'], 'tmp/', 'tmp')
        video_file.name = video.title + '.mp4'
        video.video = video_file

        # mp4 to wav
        mp4 = mp.VideoFileClip('tmp/tmp.mp4')
        mp4.audio.write_audiofile('tmp/tmp.wav')

        # audio_file 할당
        audio_filename = video_file.name.replace('.mp4', '.wav')
        audio_file = File(open('tmp/tmp.wav', 'rb'))
        video.audio.save(audio_filename, audio_file)

        video.save()

        response = recognize_by_google_stt(str(video.audio))

        # 인식된 word 를 db에 저장
        for text, start_at, end_at in get_timestamp(response):
            Word(text=text, start_at=start_at, end_at=end_at,
                 video=video).save()
            print(text, start_at, end_at, '저장완료')

        return HttpResponse('완료')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('list')
        else:
            error_msg = '잘못된 정보입니다.'
            return render(request, 'login.html', {'error_msg': error_msg})


@login_required
def ajax_match(request):
    user = request.user
    find_text = request.GET.get('find_text', '')
    words = Word.objects.filter(video__user=user,
                                text__startswith=find_text)
    response_words_list = list(words.values_list('text', flat=True).distinct())
    return JsonResponse({'words_list': response_words_list})



