from django.contrib import admin
from django.urls import path, include, re_path

from unrest.views import index
from server.views import channel_list, sponsor_list, sponsor_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/channels/', channel_list),
    path('api/sponsors/', sponsor_list),
    path('api/sponsor/<int:sponsor_id>/', sponsor_detail),
    path('', include('social_django.urls', namespace='social')),
    path('', include('unrest.urls')),
    re_path('', index),
]
