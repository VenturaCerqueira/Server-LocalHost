#!/usr/bin/env python3
"""
Script to create the system_links table for the portal area.
"""

import sys
import os

# Add the parent directory to the path to import the app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from servidor_app import create_app, db
from servidor_app.models.system_link_model import SystemLink

def create_system_links_table():
    """Create the system_links table if it doesn't exist."""
    app = create_app()

    with app.app_context():
        try:
            # Drop the existing table to apply schema changes (icon field)
            SystemLink.__table__.drop(db.engine, checkfirst=True)
            # Create the table with updated schema
            db.create_all()
            print("Tabela 'system_links' recriada com sucesso com o campo 'icon'.")
        except Exception as e:
            print(f"Erro ao recriar tabela 'system_links': {e}")
            return False

    return True

if __name__ == '__main__':
    success = create_system_links_table()
    if success:
        print("Script executado com sucesso.")
    else:
        print("Falha na execução do script.")
        sys.exit(1)
