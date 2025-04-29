const photoSelect = document.getElementById('photo-select');
const originalImage = document.getElementById('original-image');
const imagePreviewContainer = document.getElementById('image-preview-container');
const filtersSection = document.getElementById('filters-section');
const applySection = document.getElementById('apply-section');
const resultSection = document.getElementById('result-section');
const resultImage = document.getElementById('result-image');
let selectedFilter = null;
photoSelect.addEventListener('change', function() {
    if (this.value) {
        const imageUrl = `/media/${this.value}`;
        originalImage.src = imageUrl;
        
        // Ждем загрузки изображения
        originalImage.onload = function() {
            // Устанавливаем стили для правильного отображения
            originalImage.style.maxWidth = '100%';
            originalImage.style.maxHeight = '30vh';
            originalImage.style.width = 'auto';
            originalImage.style.height = 'auto';
            originalImage.style.objectFit = 'contain';
            
            imagePreviewContainer.classList.remove('hidden');
            filtersSection.classList.remove('hidden');
        };
    } else {
        imagePreviewContainer.classList.add('hidden');
        filtersSection.classList.add('hidden');
        applySection.classList.add('hidden');
        resultSection.classList.add('hidden');
    }
});

document.querySelectorAll('.filter-option').forEach(option => {
    option.addEventListener('click', function() {
        document.querySelectorAll('.filter-option').forEach(opt => {
            opt.classList.remove('ring-2', 'ring-amber-500');
        });
        this.classList.add('ring-2', 'ring-amber-500');
        selectedFilter = this.dataset.filter;
        applySection.classList.remove('hidden');
    });
});

document.getElementById('apply-filter').addEventListener('click', function() {
    const photoId = document.getElementById('photo-select').value;
    const maskType = selectedFilter;
    
    if (!photoId || !maskType) {
        alert('Выберите фото и фильтр!');
        return;
    }

    const formData = new FormData();
    formData.append('photo_id', photoId);
    formData.append('mask_type', maskType);

    fetch('/opencv/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }
        
        originalImage.src = data.original_photo_url;
        resultImage.src = data.processed_photo_url;
        resultSection.classList.remove('hidden');
        resultImage.onload = function() {
            resultImage.style.maxWidth = '100%';
            resultImage.style.maxHeight = '30vh';
            resultImage.style.width = 'auto';
            resultImage.style.height = 'auto';
            resultImage.style.objectFit = 'contain';
        };
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Произошла ошибка при обработке фото');
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.getElementById('reset-btn').addEventListener('click', function() {
    photoSelect.value = '';
    imagePreviewContainer.classList.add('hidden');
    filtersSection.classList.add('hidden');
    applySection.classList.add('hidden');
    resultSection.classList.add('hidden');
    document.querySelectorAll('.filter-option').forEach(opt => {
        opt.classList.remove('ring-2', 'ring-amber-500');
    });
    selectedFilter = null;
});

document.getElementById('download-btn').addEventListener('click', function() {
    alert('Функция скачивания реализован НЕ БУДЕТ');
});