import os
from flask import Flask
from config import Config
from app.models import db

def create_app():
    base_dir = os.path.abspath(os.path.dirname(__file__))  
    templates_dir = os.path.join(base_dir, "..", "templates")  # Путь к templates
    static_dir = os.path.join(base_dir, "..", "static")  # Путь к static

    app = Flask(__name__, template_folder=templates_dir, static_folder=static_dir)
    app.config.from_object(Config)

    db.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    # Создаем таблицы в базе данных при старте приложения
    with app.app_context():
        db.create_all()

    return app
