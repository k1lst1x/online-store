from app import create_app
from app.models import db, User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    if not User.query.filter_by(username="admin").first():
        admin_user = User(username="admin", password=generate_password_hash("admin"), is_admin=True)
        db.session.add(admin_user)
        db.session.commit()
        print("Администратор создан: admin / admin")
