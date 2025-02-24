import os
from flask import Flask, redirect, url_for, request
from config import Config
from app.models import db
from app.admin import admin
from flask_login import LoginManager, current_user
from app.models import User

def create_app():
    base_dir = os.path.abspath(os.path.dirname(__file__))  
    templates_dir = os.path.join(base_dir, "..", "templates")  # Путь к templates
    static_dir = os.path.join(base_dir, "..", "static")  # Путь к static

    app = Flask(__name__, template_folder=templates_dir, static_folder=static_dir)
    app.config.from_object(Config)

    db.init_app(app)

    # Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"  # Перенаправление на страницу входа

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.before_request
    def restrict_admin_access():
        if request.path.startswith("/admin") and not current_user.is_authenticated:
            return redirect(url_for("auth.login"))

    admin.init_app(app)

    from app.routes import main
    from app.auth import auth
    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix="/auth")

    # Создаем таблицы в базе данных при старте приложения
    with app.app_context():
        db.create_all()

    return app
