#!/usr/bin/env python3
"""
Script to create the FileMetadata table in the database.
Run this script to add the new table for tracking file ownership and updates.
"""

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from servidor_app import create_app, db
from servidor_app.models.file_metadata_model import FileMetadata

def create_file_metadata_table():
    """Create the FileMetadata table if it doesn't exist."""
    app = create_app()

    with app.app_context():
        try:
            # Create the table
            db.create_all()
            print("FileMetadata table created successfully!")

            # Verify the table was created
            inspector = db.inspect(db.engine)
            if 'file_metadata' in inspector.get_table_names():
                print("✓ FileMetadata table verified in database")
            else:
                print("✗ FileMetadata table not found in database")

        except Exception as e:
            print(f"Error creating FileMetadata table: {e}")
            return False

    return True

if __name__ == "__main__":
    print("Creating FileMetadata table...")
    success = create_file_metadata_table()
    if success:
        print("Migration completed successfully!")
    else:
        print("Migration failed!")
        sys.exit(1)
