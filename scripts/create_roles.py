import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from servidor_app import create_app, db
from servidor_app.models.user_model import User
from servidor_app.models.role_model import Role
import json

app = create_app()
app.app_context().push()

# Create roles table if it doesn't exist
db.create_all()

# Define default roles with allowed areas
default_roles = [
    {
        'name': 'admin',
        'allowed_areas': ['meus_arquivos', 'banco_dados', 'sistemas', 'licitacoes', 'dropbox', 'metrics', 'performance', 'admin']
    },
    {
        'name': 'licitacao',
        'allowed_areas': ['meus_arquivos', 'licitacoes', 'dropbox']
    },
    {
        'name': 'sistemas',
        'allowed_areas': ['meus_arquivos', 'banco_dados', 'sistemas', 'dropbox']
    },
    {
        'name': 'viewer',
        'allowed_areas': ['meus_arquivos']
    }
]

# Create roles if they don't exist
for role_data in default_roles:
    role = Role.query.filter_by(name=role_data['name']).first()
    if not role:
        role = Role(
            name=role_data['name'],
            allowed_areas=json.dumps(role_data['allowed_areas'])
        )
        db.session.add(role)
        print(f"Role '{role_data['name']}' created.")
    else:
        print(f"Role '{role_data['name']}' already exists.")

# Assign admin role to user 'keep' if exists
keep_user = User.query.filter_by(username='keep').first()
if keep_user:
    admin_role = Role.query.filter_by(name='admin').first()
    if admin_role:
        keep_user.role = admin_role
        db.session.commit()
        print("Admin role assigned to user 'keep'.")
    else:
        print("Admin role not found.")

db.session.commit()
print("Roles setup completed.")
