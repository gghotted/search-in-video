from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect, reverse
from django.views.generic import View, CreateView, ListView
from django.core.files import File
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import Length

from .models import Video, Word
from .youtube import MyYoutube
from .tasks import abstract_words_process
from .util import load_as_tempfile

from account.models import User

import tempfile


class IndexView(LoginRequiredMixin, ListView):
    model = Video
    template_name = 'main/index.html'
    context_object_name = 'videos'

    def get_queryset(self):
        user = self.request.user
        videos = Video.objects.filter(user=user)
        return videos


class UploadView(LoginRequiredMixin, View):
    def get(self, request, source_type='choice'):
        template_name = 'main/upload_' + source_type.replace('-', '_') + '.html'
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


class ListView(LoginRequiredMixin, ListView):
    model = Video
    template_name = 'main/list.html'
    context_object_name = 'videos'

    def get_queryset(self):
        user = self.request.user
        find_text = self.request.GET.get('find_text')
        videos = Video.objects.filter(
            user=user,
            words__text__icontains=find_text,
        ).distinct()
        return videos
