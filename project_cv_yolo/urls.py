from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('upload/', views.upload_photo, name='upload_photo'),
    path('opencv/', views.photo_mask, name='photo_mask'),
    path('video/', views.video, name='video'),
    path('upload-video/', views.upload_video, name='upload_video'),
    path('video-feed/', views.video_feed, name='video_feed'),
    path('detections/', views.detections_api, name='detections_api'),
    path('', views.welcome, name='welcome'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('gallery/delete/<int:photo_id>/', views.delete_photo, name='delete_photo'),
]