from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.models import db, Product, Feedback

admin = Admin(name="Admin Panel", template_mode="bootstrap4")

admin.add_view(ModelView(Product, db.session, name="Товары"))
admin.add_view(ModelView(Feedback, db.session, name="Обратная связь"))
