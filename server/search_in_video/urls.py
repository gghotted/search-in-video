from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('list', views.ListView.as_view(), name='list'),
    path('upload', views.UploadView.as_view(), name='upload'),
    path('upload/<str:method>', views.UploadView.as_view(), name='upload'),
    path('signup', TemplateView.as_view(template_name='signup.html'), name='signup'),
    path('login', views.LoginView.as_view(), name='login'),
    path('ajax/match', views.ajax_match, name='match'),
]
