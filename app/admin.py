from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask_admin.menu import MenuLink
from flask import redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

from app.models import db, Product, Feedback, User

class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        flash("Доступ запрещен! Войдите как администратор.", "danger")
        return redirect(url_for("auth.login"))

class UserAdmin(ModelView):
    column_list = ("id", "username", "is_admin")  # Отображаемые поля
    form_columns = ("username", "password", "is_admin")  # Поля для редактирования

    def on_model_change(self, form, model, is_created):
        """Хеширует пароль, если он изменился"""
        if form.password.data:
            if not check_password_hash(model.password, form.password.data):  # Проверяем, не хеширован ли уже пароль
                model.password = generate_password_hash(form.password.data)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        flash("Доступ запрещен! Войдите как администратор.", "danger")
        return redirect(url_for("auth.login"))

admin = Admin(name="Admin Panel", template_mode="bootstrap4")

admin.add_view(AdminModelView(Product, db.session, name="Товары"))
admin.add_view(AdminModelView(Feedback, db.session, name="Обратная связь"))
admin.add_view(UserAdmin(User, db.session, name="Пользователи"))  # Используем кастомный UserAdmin

class LoginMenuLink(MenuLink):

    def is_accessible(self):
        return not current_user.is_authenticated 


class LogoutMenuLink(MenuLink):

    def is_accessible(self):
        return current_user.is_authenticated             

admin.add_link(LogoutMenuLink(name='Logout', category='', url="/auth/logout"))
admin.add_link(LoginMenuLink(name='Login', category='', url="/auth/login"))