from app import create_app, db
from app.models import Admin

app = create_app()
with app.app_context():
    # Create admin object
    admin = Admin(username='admin')  # Replace with your desired username
    admin.set_password('admin123')   # Replace with your desired password

    # Add to DB
    db.session.add(admin)
    db.session.commit()

    print("Admin user created successfully!")
