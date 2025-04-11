from django import forms

from .models import PhotoModel

#Form for photo upload
class PhotoModelForm(forms.ModelForm):
    class Meta:
        model = PhotoModel
        fields = ['title', 'image']