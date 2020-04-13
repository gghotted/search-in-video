from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.views.generic import View
from django.core.files import File
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Length

from .models import Video, Word
from .youtube import MyYoutube
from .tasks import abstract_words_process
from .util import load_as_tempfile

import tempfile


# test
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
            videos = videos.filter(words__text__icontains=find_text).order_by(Length('words__text')).distinct()

        return render(request, 'list.html', {'videos': videos})


class UploadView(View):
    def get(self, request, source_type='choice'):
        template_name = 'upload_' + source_type.replace('-', '_') + '.html'
        return render(request, template_name)


    def post(self, request, source_type):
        user = request.user
        title = request.POST.get('title')
        youtube_link = request.POST.get('youtube_link')
        videofile = request.FILES.get('file')

        video = Video.objects.create(user=user,
                                     title=title,
                                     source_type=source_type,
                                     youtube_link=youtube_link,
                                     state='대기중')

        videofile_path = load_as_tempfile(videofile) if videofile else None
        abstract_words_process.delay(video_id=video.id,
                                     videofile_path=videofile_path)

        return HttpResponseRedirect('/state/uploading/list')


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
                                text__icontains=find_text)
    response_words_list = list(words.values_list('text', flat=True).order_by(Length('text')).distinct())
    return JsonResponse({'words_list': response_words_list})



