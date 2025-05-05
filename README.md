# 🍑 Peaches YOLO + OpenCV — Анализ изображений и видео в браузере

Проект "Peach Photography" — это веб-интерфейс для загрузки фотографий и видеороликов с последующим их анализом с помощью YOLOv11 и OpenCV. Реализован на базе Django, использует Tailwind CSS и Font Awesome для стиля. Все данные обрабатываются локально или в докер-контейнере.

---

## 🌟 Функционал

✅ Загрузка отдельных фотографий  
✅ Галерея с просмотром и удалением  
✅ Анализ видеороликов с выводом детекций в реальном времени  
✅ Итоговая статистика по объектам после окончания видео  
✅ Поддержка Docker и Postgres  

---

## 📦 Технологии

- **Python 3.12**
- **Django 4.x** — веб-фреймворк
- **ultralytics (YOLOv11)** — детекция объектов
- **OpenCV** — обработка кадров
- **Tailwind CSS** + **Font Awesome** — стили и иконки
- **Docker / docker-compose** — контейнеризация
- **PostgreSQL** — хранение данных

---


---

## 🛠️ Установка

### 0. Предустановки.
- Обязательно ознакомься с документацией по YOLO https://docs.ultralytics.com/usage/python/ и помести сохраненную модель в папку model/ (её нужно создать ручками)
- По-хорошему, необходимо ознакомиться с документацией Django https://docs.djangoproject.com/en/5.2/
- Установи Python, если еще нет (почему ты тут, если этого нет)))) ) https://www.python.org/

### 1. Клонируй репозиторий:
```bash
git clone https://github.com/YOUR_USERNAME/peach-photography.git
cd peach-photography
```

### 2. Настрой .env:
Создай .env файл в корне проекта (на будущее, если добавишь переменные среды).
Обязательно создай такие сущности, как
- POSTGRES_NAME - название бд
- POSTGRES_USER - пользователь бд
- POSTGRES_PASSWORD - пароль от пользователя и бд
- POSTGRES_HOST - хост бд (в данном случае лучше указать название из docker *db*)
- POSTGRES_PORT - порт, который используется для бд

### 3. Собери докер образ
```bash
docker-compose up --build
```

### 4. Не забудь применить все миграции из Django
```bash
Выйди из контейнера, после сборки (Ctrl+Z)
docker-compose run web python manage.py makemigrations
docker-compose run web python manage.py migrate
## НЕ ЗАБУДЬ ВНЕСТИ ИЗМЕНЕНИЯ В ДОБАВЛЕНИЕ ПОЛЕЙ В ПОСТГРЮ
INSERT INTO project_cv_yolo_masktype (maskname) VALUES ('grayscale'), ('edges'), ('hsv'), ('lab'), ('luv'), ('rgb'), ('binary'), ('gauss');
```

### 5. После этого запусти проект и перейди в бразуере на http://localhost:8000 (или другой порт, который указан в Dockerfile)
```bash
docker-compose up
```

## 👨‍💻 Автор
### MKB3ar
### GitHub: github.com/MKB3ar
### Email: pandakenfire@gmail.com
