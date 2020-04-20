from django.urls import path
from .views import search_words, serach_userid


app_name = 'search'

urlpatterns = [
    path('words', search_words, name='words'),
    path('userid', serach_userid, name='userid'),
] 