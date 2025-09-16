#!/usr/bin/env python3
"""
Test script for production MySQL database listing
"""
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from servidor_app.services.database_service import list_production_mysql_databases

def test_production_db_connection():
    """Test the production database connection and listing"""
    # Mock config with the provided credentials
    config = {
        'MYSQL_HOST': 'db-keepsistemas-sql8.c3emmyqhonte.sa-east-1.rds.amazonaws.com',
        'MYSQL_PORT': 3306,
        'MYSQL_USER': 'servidor',
        'MYSQL_PASSWORD': "servkinfo2013"
    }

    print("Testing production MySQL database connection...")
    print(f"Host: {config['MYSQL_HOST']}")
    print(f"Port: {config['MYSQL_PORT']}")
    print(f"User: {config['MYSQL_USER']}")
    print(f"Password: {'*' * len(config['MYSQL_PASSWORD'])}")
    print()

    result = list_production_mysql_databases(config)

    print("Result:")
    print(f"Success: {result['success']}")
    if result['success']:
        print(f"Databases found: {len(result['databases'])}")
        print("Databases:")
        for db in result['databases']:
            print(f"  - {db}")
    else:
        print(f"Error: {result['error']}")
        if 'details' in result:
            print(f"Details: {result['details']}")
        if 'suggestion' in result:
            print(f"Suggestion: {result['suggestion']}")

if __name__ == "__main__":
    test_production_db_connection()
