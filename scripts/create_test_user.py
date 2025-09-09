from servidor_app import create_app, db
from servidor_app.models.user_model import User

app = create_app()
app.app_context().push()

def create_test_user():
    username = "testuser"
    email = "testuser@example.com"
    password = "newpassword123"

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        existing_user.set_password(password)
        db.session.commit()
        print("Test user password reset successfully.")
        return

    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    print("Test user created successfully.")

if __name__ == "__main__":
    create_test_user()
