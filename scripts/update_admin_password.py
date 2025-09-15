#!/usr/bin/env python3
"""
Script para atualizar a senha do usuário administrador 'keep' para 'kinfo2013'
"""
import os
import sys

# Adicionar o diretório do projeto ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from servidor_app import create_app, db
from servidor_app.models.user_model import User

def update_admin_password():
    """Atualiza a senha do usuário administrador 'keep'"""
    app = create_app()

    with app.app_context():
        # Verificar se o usuário existe
        user = User.query.filter_by(username='keep').first()

        if not user:
            print("Usuário 'keep' não encontrado.")
            return

        # Atualizar a senha
        user.set_password('kinfo2013')
        db.session.commit()

        print("Senha do usuário 'keep' atualizada para 'kinfo2013'.")

if __name__ == '__main__':
    update_admin_password()
