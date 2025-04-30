from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.core.files.storage import default_storage

# Create your models here.

#Model for photo in database
class PhotoModel(models.Model):
    title = models.CharField(
        max_length=100,
        blank=True
    )
    image = models.ImageField(
        upload_to='photo/'
    )
    uploaded_at = models.DateTimeField(
        default=timezone.now
    )
    
    def delete(self, *args, **kwargs):
    # Удаляем основное фото
        if self.image:
            if default_storage.exists(self.image.name):
                default_storage.delete(self.image.name)
        # Удаляем все связанные ProcessedPhoto и их файлы
        for processed in self.processedphoto_set.all():
            if default_storage.exists(processed.processed_photo.name):
                default_storage.delete(processed.processed_photo.name)
            processed.delete()
        super().delete(*args, **kwargs)
    
    def __str__(self):
        return self.title + ' ' + str(self.image)
    
#Model for masktype in cv2
class MaskType(models.Model):
    maskname = models.CharField()
    
#Model for processed photo with cv2
class ProcessedPhoto(models.Model):
    original_photo = models.ForeignKey(
        PhotoModel, on_delete=models.CASCADE
    )
    processed_photo = models.ImageField(
        upload_to='processed_photo/',
        max_length=255
    )
    mask_type = models.ForeignKey(
        MaskType, on_delete=models.RESTRICT
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

class VideoModel(models.Model):
    title = models.CharField(max_length=100, blank=True)
    video = models.FileField(upload_to='video/',
                             validators=[FileExtensionValidator(['mp4'])])
    uploaded_at = models.DateTimeField(default=timezone.now)
