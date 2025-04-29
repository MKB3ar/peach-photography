import os
import cv2

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, StreamingHttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.conf import settings
from ultralytics import YOLO


from .models import PhotoModel, ProcessedPhoto, MaskType
from .forms import PhotoModelForm
from .utils import apply_mask
# Create your views here.

camera = cv2.VideoCapture(0)
model = YOLO(model="project_cv_yolo/model/yolo11n.pt")
last_detections = {}

@csrf_exempt
def upload_photo(request):
    if request.method == 'POST':
        form = PhotoModelForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            photo = form.save()
            return JsonResponse({
                    'status': 'success',
                    'message': 'Фото успешно загружено!',
                    'photo_id': photo.id,
                    'photo_name': photo.title,
                    'photo_url': photo.image.url  # Предполагается, что у модели есть поле image
                })
        else:
            return JsonResponse({
                    'status': 'error',
                    'message': 'Ошибка валидации формы',
                    'errors': form.errors
                }, status=400)
    form = PhotoModelForm()
    return render(
        request=request,
        context={'form':form},
        template_name='project_cv_yolo/test_upload.html'
        )
    
def photo_mask(request):
    photos = PhotoModel.objects.all()  # Получаем список всех фото

    if request.method == 'POST':
        photo_id = request.POST.get('photo_id')
        mask_type = request.POST.get('mask_type')

        original_photo = PhotoModel.objects.filter(
            image=photo_id
        ).first()
        mask = MaskType.objects.filter(
            maskname = mask_type
        ).first()
        
        entry = ProcessedPhoto.objects.filter(
            original_photo = original_photo,
            mask_type = mask
        ).first()
        
        if entry:
            return JsonResponse({
                'processed_photo_url': entry.processed_photo.url,
                'original_photo_url': original_photo.image.url,
                'mask_type': mask_type
            })
        
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
        return JsonResponse({
            'processed_photo_url': processed_photo.processed_photo.url,
            'original_photo_url': original_photo.image.url,
            'mask_type': mask_type
        })

    return render(request, 'project_cv_yolo/test_opencv.html', {'photos': photos})  # Возвращаем список фото

def video_feed(request):
    return StreamingHttpResponse(gen_frames(), content_type='multipart/x-mixed-replace; boundary=frame')

def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        result = model(frame,
                       verbose=False)
        result_frame = result[0].plot()  # This returns an image with the bounding boxes drawn
        
        # Извлекаем классы обнаруженных объектов
        boxes = result[0].boxes

        class_ids = boxes.cls.cpu().numpy().astype(int)
        confidences = boxes.conf.cpu().numpy()

        class_names = model.names  # Словарь: id -> имя класса

        # Собираем словарь: имя класса -> список вероятностей
        detections = {}
        for cls_id, conf in zip(class_ids, confidences):
            name = class_names[cls_id]
            if name not in last_detections:
                last_detections[name] = []
            last_detections[name].append(conf * 100)


        _, buffer = cv2.imencode('.jpg', result_frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    camera.release()

def video(request):
    print("=== ЗАПУСКАЕТСЯ view 'video' ===")
    return render(request, 'project_cv_yolo/video.html')


def detections_api(request):
    global last_detections
    response_data = {
        name: round(sum(confs) / len(confs), 1)
        for name, confs in last_detections.items()
    }
    return JsonResponse(response_data)

def welcome(request):
    return render(request, 'project_cv_yolo/welcome_page.html')
