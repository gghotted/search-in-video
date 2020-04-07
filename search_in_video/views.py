from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import View
from django.core.files import File
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import Video, Word
from .util import OverwriteStorage, recognize_by_google_stt, get_timestamp
from .youtube import MyYouTube
from .tasks import recognize_video_process

# import moviepy.editor as mp


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
    def get(self, request, source_type='choice'):
        template_name = 'upload_' + source_type.replace('-', '_') + '.html'
        return render(request, template_name)


    def post(self, request, source_type):
        # video file을 저장한다
        self.save_videofile_by_source_type(source_type,
                                           videofile=request.FILES.get('file'),
                                           youtube_link=request.POST.get('youtube_link'))

        # audio file을 추출한다

        # cloud storage에 저장한다

        # stt api를 실행한다

        # 결과를 db에 저장한다

        return HttpResponse('완료')

    
    def save_videofile_by_source_type(self, source_type, **kwargs):
        if source_type == 'user-pc':
            videofile = kwargs['videofile']
            OverwriteStorage('tmp/').save('tmp.mp4', videofile)
        elif source_type == 'youtube-link':
            yt = MyYouTube(kwargs['youtube_link'])
            yt.download_best_video('tmp/', 'tmp')



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



