class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Отключаем отслеживание изменений
    SECRET_KEY = 'your_secret_key'
    UPLOAD_FOLDER = 'uploads'