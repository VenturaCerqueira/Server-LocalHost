#!/usr/bin/env python3
"""
Simple test script to check system links and blocks.
"""

import sys
import os

# Add the parent directory to the path to import the app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from servidor_app import create_app, db
from servidor_app.models.system_link_model import SystemLink

def test_blocks():
    """Test function to check blocks."""
    app = create_app()

    with app.app_context():
        try:
            # Get total count
            total_links = SystemLink.query.count()
            print(f"Total de links do sistema: {total_links}")

            if total_links > 0:
                # Get all links
                links = SystemLink.query.all()
                print("\nLinks existentes:")
                for link in links:
                    print(f"- {link.name} (Bloco: {link.block or 'Nenhum'})")

                # Get distinct blocks
                distinct_blocks = db.session.query(SystemLink.block).distinct().all()
                distinct_blocks = [row[0] for row in distinct_blocks if row[0]]

                print(f"\nBlocos distintos: {distinct_blocks}")
            else:
                print("Nenhum link encontrado. Adicionando links de exemplo...")

                # Add sample links
                sample_links = [
                    SystemLink(name='Sistema Admin', url='http://localhost/admin', block='Administração', icon='bi bi-gear'),
                    SystemLink(name='Relatórios', url='http://localhost/reports', block='Relatórios', icon='bi bi-graph-up'),
                    SystemLink(name='Base de Dados', url='http://localhost/db', block='Dados', icon='bi bi-database'),
                ]

                for link in sample_links:
                    db.session.add(link)

                db.session.commit()
                print("Links de exemplo adicionados!")

                # Get blocks again
                distinct_blocks = db.session.query(SystemLink.block).distinct().all()
                distinct_blocks = [row[0] for row in distinct_blocks if row[0]]
                print(f"Blocos criados: {distinct_blocks}")

        except Exception as e:
            print(f"Erro: {e}")
            return False

    return True

if __name__ == '__main__':
    test_blocks()
