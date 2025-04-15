import os
import cv2

from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.conf import settings

from .models import PhotoModel, ProcessedPhoto, MaskType
from .forms import PhotoModelForm
from .utils import apply_mask
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
        template_name='project_cv_yolo/upload.html'
        )

def photo_mask(request):
    photos = PhotoModel.objects.all()  # Получаем список всех фото

    if request.method == 'POST':
        photo_id = request.POST.get('photo_id')
        mask_type = request.POST.get('mask_type')

        original_photo = PhotoModel.objects.filter(
            id=photo_id
        ).first()
        mask = MaskType.objects.filter(
            maskname = mask_type
        ).first()
        
        entry = ProcessedPhoto.objects.filter(
            original_photo = original_photo,
            mask_type = mask
        ).first()
        
        if entry:
            print(original_photo.image.url)
            print(entry.processed_photo.url)
            return render(
                request=request,
                template_name='project_cv_yolo/opencv.html',
                context={
                    'photos': photos,
                    'original_image': original_photo.image.url,
                    'processed_photo': entry.processed_photo.url,
                    'mask_type': mask_type
                }
            )
        
        processed_image = apply_mask(original_photo.image.url, mask_type)
        
        
        processed_dir = os.path.join(settings.MEDIA_ROOT, 'processed_photo')
        os.makedirs(processed_dir, exist_ok=True)
        
        processed_filename = f"{mask_type}_{os.path.basename(original_photo.image.url)}"
        processed_image_path = os.path.join(processed_dir, processed_filename)
        
        cv2.imwrite(processed_image_path, processed_image)

        processed_photo = ProcessedPhoto(
            original_photo = original_photo,
            mask_type=mask,
            processed_photo = f'processed_photo/{processed_filename}'
        )
        processed_photo.save()
        return render(
            request=request,
            template_name='project_cv_yolo/opencv.html',
            context={
                'photos': photos,
                'original_image': original_photo.image.url,
                'processed_photo': ProcessedPhoto.processed_photo,
                'mask_type': mask_type
                }
            )

    return render(request, 'project_cv_yolo/opencv.html', {'photos': photos})  # Возвращаем список фото