# Flask приложение файлообменник

## Описание
Этот проект предоставляет удобный сервис для загрузки файлов, их сжатия и обмена.

### Стек
- Flask
- Celery
- Redis: брокер сообщений для Celery.
- bz2: для сжатия файлов.

### Основные функции:
1. **Загрузка файлов:** Пользователи могут загружать файлы через удобный веб-интерфейс.
2. **Сжатие файлов:** После загрузки файл автоматически передаётся в очередь задач Celery через Redis и сжимается с использованием алгоритма bz2.
3. **Совместное использование:**
   - Пользователь может указать, каким юзерам (по их юзернеймам) будет доступен файл.
   - Также генерируется уникальная ссылка, которую можно скопировать и поделиться с другими.
---

### Структура
![Схема взаимодействия](https://github.com/nezhdanchik/file-storage/blob/main/structure.png)

## Установка и настройка

Создайте файл `.env` в корневой директории проекта и добавьте в него следующие переменные:
```
CELERY_BROKER_HOST=localhost
CELERY_BROKER_PORT=6379
```

Затем запустите с помощью docker-compose
```bash
$ docker-compose up --build
```

Приложение будет доступно по адресу: `http://127.0.0.1:8000`

