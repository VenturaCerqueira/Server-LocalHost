#!/usr/bin/env python3
"""
Script para criar usuário administrador 'keep' com senha 'kinfo2013'
"""
import os
import sys

# Adicionar o diretório do projeto ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from servidor_app import create_app, db
from servidor_app.models.user_model import User

def create_admin_user():
    """Cria o usuário administrador se não existir"""
    app = create_app()

    with app.app_context():
        # Verificar se o usuário já existe
        existing_user = User.query.filter_by(username='keep').first()

        if existing_user:
            print("Usuário 'keep' já existe.")
            # Atualizar para admin se não for
            if not existing_user.is_admin:
                existing_user.is_admin = True
                existing_user.is_active = True
                db.session.commit()
                print("Usuário 'keep' atualizado para administrador.")
            return

        # Criar novo usuário admin
        admin_user = User(username='keep', is_admin=True, is_active=True)
        admin_user.set_password('kinfo2013')

        db.session.add(admin_user)
        db.session.commit()

        print("Usuário administrador 'keep' criado com sucesso!")
        print("Senha: kinfo2013")

if __name__ == '__main__':
    create_admin_user()
