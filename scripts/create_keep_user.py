import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from servidor_app import create_app, db
from servidor_app.models.user_model import User
from servidor_app.models.role_model import Role

app = create_app()
app.app_context().push()

def create_keep_user():
    username = "keep"
    email = "keep@example.com"
    password = "newpassword123"  # Reset password to a known value

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        existing_user.set_password(password)
        db.session.commit()
        print("User 'keep' password reset successfully.")
        return

    new_user = User(username=username, email=email)
    new_user.set_password(password)

    # Assign admin role
    admin_role = Role.query.filter_by(name='admin').first()
    if admin_role:
        new_user.role = admin_role

    db.session.add(new_user)
    db.session.commit()
    print("User 'keep' created successfully with admin role.")

if __name__ == "__main__":
    create_keep_user()
