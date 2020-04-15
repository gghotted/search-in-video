from django.urls import path
from . import views
from django.views.generic import TemplateView


app_name = 'main'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('list', views.ListView.as_view(), name='list'),
    path('upload', views.UploadView.as_view(), name='upload'),
    path('upload/<str:source_type>', views.UploadView.as_view(), name='upload'),
    path('ajax/match', views.ajax_match, name='match'),
    path('ajax/userid', views.ajax_userid)
]
