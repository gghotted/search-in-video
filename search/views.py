from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models.functions import Length

from main.models import Word
from account.models import User


@login_required
def search_words(request):
    user = request.user
    find_text = request.GET.get('find_text', '')
    words = Word.objects.filter(video__user=user,
                                text__icontains=find_text)
    response_words_list = list(words.values_list('text', flat=True).order_by(Length('text')).distinct())[:10]
    return JsonResponse({'words_list': response_words_list})


def serach_userid(request):
    username = request.GET.get('username')
    get_user = User.objects.filter(username=username)
    if len(get_user) == 0:
        return JsonResponse({'result': True})
    return JsonResponse({'result': False})
