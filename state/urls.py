from django.urls import path
from . import views

urlpatterns = [
    path('uploading/list', views.UploadingListView.as_view()),
]