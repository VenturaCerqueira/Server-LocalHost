#!/usr/bin/env python3
"""
Test script for database analysis functionality
"""
import os
import sys
sys.path.append('.')

from servidor_app import create_app

def test_analysis():
    app = create_app()

    with app.app_context():
        from servidor_app.controllers.main_controller import analyze_database

        # Test with a known database
        db_name = 'db_cnd_dam'  # Change this to a real database name

        try:
            result = analyze_database(db_name)
            print("Analysis completed successfully")
            print(f"Result type: {type(result)}")
        except Exception as e:
            print(f"Error during analysis: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_analysis()
