from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('upload/', views.upload_photo, name='upload_photo'),
    path('opencv/', views.photo_mask, name='photo_mask'),
    path('video/', views.video, name='video'),
    path('detections/', views.detections_api, name='detections_api'),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('', views.welcome, name='welcome')
]