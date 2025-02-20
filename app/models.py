from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255), nullable=False, default="/static/images/default.jpg")
    category = db.Column(db.String(50), nullable=False)  # Новое поле категория

    def __repr__(self):
        return f"<Product {self.name}>"

