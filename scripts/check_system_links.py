#!/usr/bin/env python3
"""
Script to check existing system links and their blocks.
"""

import sys
import os

# Add the parent directory to the path to import the app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from servidor_app import create_app, db
from servidor_app.models.system_link_model import SystemLink

def check_system_links():
    """Check existing system links and their blocks."""
    app = create_app()

    with app.app_context():
        try:
            # Get all system links
            links = SystemLink.query.all()
            print(f"Total de links do sistema: {len(links)}")

            if links:
                print("\nLinks existentes:")
                for link in links:
                    print(f"- ID: {link.id}, Nome: {link.name}, Bloco: {link.block or 'Nenhum'}, URL: {link.url}")

                # Get distinct blocks
                distinct_blocks = db.session.query(SystemLink.block).distinct().all()
                distinct_blocks = [row[0] for row in distinct_blocks if row[0]]

                print(f"\nBlocos distintos encontrados: {len(distinct_blocks)}")
                if distinct_blocks:
                    for block in distinct_blocks:
                        print(f"- {block}")
                else:
                    print("Nenhum bloco encontrado nos links existentes.")
            else:
                print("Nenhum link do sistema encontrado.")
                print("Será necessário criar alguns links com blocos para que apareçam no dropdown.")

        except Exception as e:
            print(f"Erro ao consultar links do sistema: {e}")
            return False

    return True

if __name__ == '__main__':
    success = check_system_links()
    if success:
        print("\nScript executado com sucesso.")
    else:
        print("\nFalha na execução do script.")
        sys.exit(1)
