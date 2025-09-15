from servidor_app import create_app, db
from servidor_app.models.user_model import User
from servidor_app.models.role_model import Role
import json

def create_test_user():
    app = create_app()
    with app.app_context():
        # Check if role 'sistemas' exists, create if not
        role = Role.query.filter_by(name='sistemas').first()
        if not role:
            role = Role(name='sistemas', allowed_areas=json.dumps(['sistemas']))
            db.session.add(role)
            db.session.commit()

        # Check if test user exists
        user = User.query.filter_by(username='testuser').first()
        if not user:
            user = User(username='testuser', email='testuser@example.com')
            user.set_password('TestPassword123')
            user.role = role
            user.is_active = True
            db.session.add(user)
            db.session.commit()
            print("Test user 'testuser' created with password 'TestPassword123'")
        else:
            print("Test user 'testuser' already exists")

if __name__ == '__main__':
    create_test_user()
