#!/usr/bin/env python3
"""
Test script for the improved search functionality
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from servidor_app.models.file_system_model import FileSystemModel
from servidor_app import create_app

def test_search():
    """Test the search functionality"""
    app = create_app()
    with app.app_context():
        # Test with a small directory for demonstration
        test_dir = os.path.join(os.path.dirname(__file__), 'servidor_app')

        if not os.path.exists(test_dir):
            print(f"Test directory {test_dir} does not exist")
            return

        fs_model = FileSystemModel(test_dir)

        # Test basic search
        print("Testing basic search...")
        results, pagination = fs_model.search("controller", page=1, per_page=10)
        print(f"Found {len(results)} results for 'controller'")
        print(f"Pagination: {pagination}")

        # Test pagination
        print("\nTesting pagination...")
        results2, pagination2 = fs_model.search("controller", page=2, per_page=5)
        print(f"Page 2 results: {len(results2)}")
        print(f"Pagination: {pagination2}")

        # Test caching (second call should be faster)
        print("\nTesting caching...")
        import time
        start_time = time.time()
        results3, pagination3 = fs_model.search("controller", page=1, per_page=10)
        end_time = time.time()
        print(f"Cached search took {end_time - start_time:.4f} seconds")
        print(f"Results match: {results == results3}")

        print("\nSearch functionality test completed successfully!")

if __name__ == "__main__":
    test_search()
