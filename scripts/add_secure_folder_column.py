#!/usr/bin/env python3
"""
Script to add password_hash column to file_metadata table for secure folders feature.
"""

import sqlite3
import os
import sys

# Add the parent directory to the path to import the app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from servidor_app import create_app

def add_secure_folder_column():
    app = create_app()

    with app.app_context():
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')

        if not os.path.exists(db_path):
            print(f"Database not found at {db_path}")
            return

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check if column already exists
        cursor.execute("PRAGMA table_info(file_metadata)")
        columns = [column[1] for column in cursor.fetchall()]

        if 'password_hash' in columns:
            print("Column 'password_hash' already exists in file_metadata table.")
            conn.close()
            return

        # Add the new column
        try:
            cursor.execute("ALTER TABLE file_metadata ADD COLUMN password_hash VARCHAR(128)")
            conn.commit()
            print("Successfully added 'password_hash' column to file_metadata table.")
        except Exception as e:
            print(f"Error adding column: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    add_secure_folder_column()
