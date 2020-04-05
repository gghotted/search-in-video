from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import View
from django.core.files import File
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import Video, Word
from .util import OverwriteStorage, recognize_by_google_stt, get_timestamp, youtube_download
from .util import VideoFileSaveManger
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
        manager = VideoFileSaveManger(save_path='tmp/')
        manager.save_by_source_type(source_type,
                                    request.FILES.get('file'),
                                    request.POST.get('youtube_link'))
        
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



