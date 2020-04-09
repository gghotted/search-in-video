from django.shortcuts import render
from django.views.generic import ListView

from search_in_video.models import Video


class UploadingListView(ListView):
    template_name = 'uploading.html'
    context_object_name = 'videos'
    model = Video

    def get_queryset(self):
        videos = self.model.objects.exclude(
            state='complete1'
        )
        return videos[:1]
