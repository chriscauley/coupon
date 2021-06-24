from django.contrib import admin
from django.urls import path, include, re_path

from unrest.views import index
from server.views import channel_list, sponsor_list, sponsor_detail, search_channels, add_channel

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/channels/', channel_list),
    path('api/sponsors/', sponsor_list),
    path('api/sponsor/<int:sponsor_id>/', sponsor_detail),
    path('api/search-channel/', search_channels),
    path('api/add-channel/', add_channel),
    path('', include('social_django.urls', namespace='social')),
    path('', include('unrest.urls')),
    re_path('', index),
]
