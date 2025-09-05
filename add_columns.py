#!/usr/bin/env python3
"""
Script para adicionar colunas is_admin e is_active à tabela user
"""
import sqlite3
import sys
import os

def add_columns():
    """Adiciona as colunas is_admin e is_active à tabela user"""
    db_path = 'servidor_app/app.db'

    if not os.path.exists(db_path):
        print("Database file not found.")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Verificar se as colunas já existem
        cursor.execute("PRAGMA table_info(user)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]

        if 'is_admin' not in column_names:
            cursor.execute("ALTER TABLE user ADD COLUMN is_admin BOOLEAN DEFAULT 0")
            print("Added column 'is_admin'")

        if 'is_active' not in column_names:
            cursor.execute("ALTER TABLE user ADD COLUMN is_active BOOLEAN DEFAULT 1")
            print("Added column 'is_active'")

        if 'email' not in column_names:
            cursor.execute("ALTER TABLE user ADD COLUMN email VARCHAR(120)")
            print("Added column 'email'")
            # Create unique index for email
            cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_user_email ON user(email)")
            print("Created unique index for email")

        conn.commit()
        conn.close()

        print("Database columns updated successfully!")

    except Exception as e:
        print(f"Error updating database: {e}")

if __name__ == '__main__':
    add_columns()
