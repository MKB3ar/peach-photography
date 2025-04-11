from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_photo, name='upload_photo')
]

