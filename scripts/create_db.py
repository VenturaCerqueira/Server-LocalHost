# create_db.py

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from servidor_app import create_app, db
from servidor_app.models.user_model import User

app = create_app()
app.app_context().push()

# Crie o banco de dados e as tabelas
db.create_all()

# Crie um usuário inicial (substitua a senha)
if not User.query.filter_by(username='admin').first():
    admin_user = User(username='admin', email='admin@example.com')
    admin_user.set_password('sua_nova_senha_segura') # TROQUE ESTA SENHA!
    db.session.add(admin_user)
    db.session.commit()
    print("Usuário 'admin' criado com sucesso!")
else:
    print("Usuário 'admin' já existe.")

print("Banco de dados 'app.db' inicializado.")