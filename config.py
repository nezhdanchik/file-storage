class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # Путь к базе данных
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Отключаем отслеживание изменений
    SECRET_KEY = 'your_secret_key'  # Ключ для сессий и CSRF
    CACHE_TYPE = 'simple'  # Простое кеширование в памяти
    CACHE_DEFAULT_TIMEOUT = 3600  # Время жизни кеша (в секундах)
    UPLOAD_FOLDER = 'uploads'