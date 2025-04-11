from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from .forms import PhotoModelForm
# Create your views here.

def upload_photo(request):
    if request.method == 'POST':
        form = PhotoModelForm(
            request.POST,
            request.FILES
        )
        if form.is_valid():
            photo = form.save(commit=False)
            photo.save()
            return HttpResponse('Всё успешно загружено!')
    else:
        form = PhotoModelForm()
    return render(
        request=request,
        context={'form':form},
        template_name='project_cv_yolo/upload.html')

