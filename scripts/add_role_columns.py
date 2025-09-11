#!/usr/bin/env python3
"""
Script para adicionar a coluna allowed_areas à tabela role
"""
import sqlite3
import sys
import os

def add_role_columns():
    """Adiciona a coluna allowed_areas à tabela role"""
    db_path = 'servidor_app/app.db'

    if not os.path.exists(db_path):
        print("Database file not found.")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Verificar se as colunas já existem
        cursor.execute("PRAGMA table_info(role)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]

        if 'allowed_areas' not in column_names:
            cursor.execute("ALTER TABLE role ADD COLUMN allowed_areas TEXT")
            print("Added column 'allowed_areas'")

        conn.commit()
        conn.close()

        print("Database role table updated successfully!")

    except Exception as e:
        print(f"Error updating database: {e}")

if __name__ == '__main__':
    add_role_columns()
