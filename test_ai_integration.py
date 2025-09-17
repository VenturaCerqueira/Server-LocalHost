#!/usr/bin/env python3
"""
Test script for AI integration in database analysis
"""

import os
import sys
sys.path.append('servidor_app')

from servidor_app import create_app
from servidor_app.controllers.main_controller import setup_gemini, analyze_table_with_ai, analyze_columns_with_ai

def test_ai_setup():
    """Test if AI setup works"""
    app = create_app()
    with app.app_context():
        try:
            print("Testing AI setup...")
            model = setup_gemini()
            print("✓ AI setup successful")
            return True
        except Exception as e:
            print(f"✗ AI setup failed: {e}")
            return False

def test_table_analysis():
    """Test table analysis with AI"""
    app = create_app()
    with app.app_context():
        try:
            print("\nTesting table analysis...")

            # Sample table data
            table_name = "users"
            columns = [
                {
                    'column_name': 'id',
                    'column_type': 'int(11)',
                    'column_key': 'PRI',
                    'is_nullable': 'NO',
                    'column_default': None,
                    'column_comment': 'Primary key'
                },
                {
                    'column_name': 'username',
                    'column_type': 'varchar(50)',
                    'column_key': '',
                    'is_nullable': 'NO',
                    'column_default': None,
                    'column_comment': 'User login name'
                },
                {
                    'column_name': 'email',
                    'column_type': 'varchar(100)',
                    'column_key': '',
                    'is_nullable': 'YES',
                    'column_default': None,
                    'column_comment': 'User email address'
                }
            ]

            table_info = {
                'engine': 'InnoDB',
                'table_rows': 1000,
                'size_mb': 5.2
            }

            result = analyze_table_with_ai(table_name, columns, table_info)
            print(f"✓ Table analysis result: {result[:100]}...")
            return True

        except Exception as e:
            print(f"✗ Table analysis failed: {e}")
            return False

def test_column_analysis():
    """Test column analysis with AI"""
    app = create_app()
    with app.app_context():
        try:
            print("\nTesting column analysis...")

            table_name = "users"
            columns = [
                {
                    'column_name': 'id',
                    'column_type': 'int(11)',
                    'column_key': 'PRI',
                    'is_nullable': 'NO',
                    'column_default': None,
                    'column_comment': 'Primary key'
                },
                {
                    'column_name': 'username',
                    'column_type': 'varchar(50)',
                    'column_key': '',
                    'is_nullable': 'NO',
                    'column_default': None,
                    'column_comment': 'User login name'
                }
            ]

            result = analyze_columns_with_ai(table_name, columns)
            print(f"✓ Column analysis result: {type(result)}")
            if isinstance(result, dict):
                print(f"  Keys: {list(result.keys())}")
            return True

        except Exception as e:
            print(f"✗ Column analysis failed: {e}")
            return False

def main():
    """Run all AI integration tests"""
    print("=== AI Integration Test ===\n")

    # Check if API key is configured
    api_key = os.environ.get('GOOGLE_API_KEY')
    if not api_key:
        print("✗ GOOGLE_API_KEY not found in environment variables")
        print("Please set your Google API key:")
        print("export GOOGLE_API_KEY=your_api_key_here")
        return False

    print(f"✓ GOOGLE_API_KEY found (length: {len(api_key)})")

    # Run tests
    tests = [
        test_ai_setup,
        test_table_analysis,
        test_column_analysis
    ]

    results = []
    for test in tests:
        results.append(test())

    print("\n=== Test Results ===")
    print(f"Passed: {sum(results)}/{len(results)}")

    if all(results):
        print("✓ All AI integration tests passed!")
        return True
    else:
        print("✗ Some tests failed. Check the output above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
