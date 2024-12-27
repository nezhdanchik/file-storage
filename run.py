from app import create_app, db

app = create_app()

# Создание контекста приложения для работы с базой данных
with app.app_context():
    db.create_all()  # Создание таблиц

if __name__ == '__main__':
    app.run(debug=True)
