from django.contrib import admin
from django.urls import path, include, re_path

from unrest.views import index
from server import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/channels/', views.channel_list),
    path('api/sponsors/', views.sponsor_list),
    path('api/sponsor/<int:sponsor_id>/', views.sponsor_detail),
    path('api/channel/<int:channel_id>/', views.channel_detail),
    path('api/search-channel/', views.search_channels),
    path('api/add-channel/', views.add_channel),
    path('', include('social_django.urls', namespace='social')),
    path('', include('unrest.urls')),
    re_path('', index),
]
