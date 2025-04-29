import cv2
import os
from django.conf import settings

def apply_mask(image_path, mask_type):
    """
    Применяет указанную маску к изображению.
    
    Args:
        image_path (str): Относительный путь к изображению от MEDIA_ROOT (например 'photo/image.jpg')
        mask_type (str): Тип маски
        
    Returns:
        Обработанное изображение
    
    Raises:
        ValueError: Если изображение не найдено или не может быть прочитано
    """
    # Полный путь к файлу
    relative_path = image_path.replace('/media/', '', 1)  # убираем /media/
    full_path = os.path.join(settings.MEDIA_ROOT, relative_path)
    
    # 2. Читаем изображение
    image = cv2.imread(full_path)
    if image is None:
        raise ValueError(f"Не удалось прочитать файл изображения: {full_path}")
    
    # Применяем маску
    if mask_type == 'grayscale':
        result = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif mask_type == 'edges':
        result = cv2.Canny(image, 100, 200)
    elif mask_type == 'hsv':
        result = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    elif mask_type == 'lab':
        result = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    elif mask_type == 'luv':
        result = cv2.cvtColor(image, cv2.COLOR_BGR2LUV)
    elif mask_type == 'rgb':
        result = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    elif mask_type == 'binary':
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        result = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                     cv2.THRESH_BINARY, 11, 2)
    elif mask_type == 'gauss':
        result = cv2.GaussianBlur(image, (25, 25), 100)
    else:
        result = image
    
    return result