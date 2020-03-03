from django.shortcuts import render, HttpResponse
from django.views import generic
from .models import Audio


class IndexView(generic.View):
    def get(self, request):
        print(Audio.objects.get(id=1).file.url)
        return render(request, 'index.html')

    def post(self, request):
        file = request.FILES['file']
        Audio(file=file).save()
        return HttpResponse('완료')

