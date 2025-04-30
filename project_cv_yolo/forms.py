from django import forms

from .models import PhotoModel, VideoModel

#Form for photo upload
class PhotoModelForm(forms.ModelForm):
    class Meta:
        model = PhotoModel
        fields = ['title', 'image']
        
class VideoForm(forms.ModelForm):
    class Meta:
        model = VideoModel
        fields = ['title', 'video']