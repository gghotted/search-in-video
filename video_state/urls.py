from django.urls import path
from . import views


app_name = 'video_state'

urlpatterns = [
    path('list', views.UploadingListView.as_view()),
]