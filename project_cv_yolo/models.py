from django.db import models
from django.utils import timezone

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
    
    def __str__(self):
        return self.title + ' ' + str(self.image)
    
#Model for masktype in cv2
class MaskType(models.Model):
    maskname = models.CharField()
    
#Model for processed photo with cv2
class ProcessedPhoto(models.Model):
    original_photo = models.ForeignKey(
        PhotoModel, on_delete=models.RESTRICT
    )
    processed_photo = models.ImageField(
        upload_to='processed_photo/'
    )
    mask_type = models.ForeignKey(
        MaskType, on_delete=models.RESTRICT
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
