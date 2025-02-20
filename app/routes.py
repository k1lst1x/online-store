import os
from flask import Blueprint, render_template, abort, request, jsonify
from app.models import db, Product

main = Blueprint("main", __name__)

@main.route("/")
def home():
    if Product.query.count() == 0:
        sample_products = [
            Product(name="Игровая мышь Razer", description="RGB, 16000 DPI", price=5990, category="Мыши", image="/static/images/mouse.jpg"),
            Product(name="Клавиатура HyperX", description="Механическая клавиатура", price=9990, category="Клавиатуры", image="/static/images/keyboard.jpg"),
            Product(name="Монитор Samsung", description="144Hz, 27 дюймов", price=29990, category="Мониторы", image="/static/images/monitor.jpg"),
            Product(name="Гарнитура Logitech", description="Игровая гарнитура", price=7990, category="Гарнитуры", image="/static/images/headset.jpg"),
        ]
        db.session.bulk_save_objects(sample_products)
        db.session.commit()

    products = Product.query.all()
    return render_template("index.html", products=products)

@main.route("/product/<int:product_id>")
def product_page(product_id):
    product = Product.query.get(product_id)
    if not product:
        abort(404)

    return render_template("product.html", product=product)

@main.route("/favorites")
def favorites_page():
    return render_template("favorites.html")

@main.route("/get_favorites", methods=["POST"])
def get_favorites():
    data = request.get_json()
    favorite_ids = data.get("favorites", [])

    products = Product.query.filter(Product.id.in_(favorite_ids)).all()
    product_list = [
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "price": p.price,
            "image": p.image
        } for p in products
    ]
    return jsonify(product_list)

@main.route("/filter_products", methods=["GET"])
def filter_products():
    category = request.args.get("category", None)
    min_price = request.args.get("min_price", type=float, default=0)
    max_price = request.args.get("max_price", type=float, default=999999)

    query = Product.query.filter(Product.price.between(min_price, max_price))

    if category and category != "all":
        query = query.filter_by(category=category)

    products = query.all()

    product_list = [
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "price": p.price,
            "image": p.image
        } for p in products
    ]

    return jsonify(product_list)
