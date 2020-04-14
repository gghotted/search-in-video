from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('list', views.ListView.as_view(), name='list'),
    path('upload', views.UploadView.as_view(), name='upload'),
    path('upload/<str:source_type>', views.UploadView.as_view(), name='upload'),
    path('signup', views.CreateUserView.as_view(), name='signup'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('ajax/match', views.ajax_match, name='match'),
    path('ajax/userid', views.ajax_userid)
]
