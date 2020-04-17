from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('main.urls')),
    path('search/', include('search.urls')),
    path('account/', include('account.urls')),
    path('video/state/', include('video_state.urls')),
    path('admin/', admin.site.urls),
]
