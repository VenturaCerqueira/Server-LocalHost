#!/usr/bin/env python3
"""
Script to add sample system links with blocks for testing the portal functionality.
"""

import sys
import os

# Add the parent directory to the path to import the app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from servidor_app import create_app, db
from servidor_app.models.system_link_model import SystemLink

def add_sample_system_links():
    """Add sample system links with different blocks."""
    app = create_app()

    with app.app_context():
        try:
            # Sample links with different blocks
            sample_links = [
                {
                    'name': 'Sistema de Gestão',
                    'url': 'http://localhost/sistema-gestao',
                    'icon': 'bi bi-gear',
                    'block': 'Administração'
                },
                {
                    'name': 'Portal de Relatórios',
                    'url': 'http://localhost/relatorios',
                    'icon': 'bi bi-graph-up',
                    'block': 'Relatórios'
                },
                {
                    'name': 'Base de Dados',
                    'url': 'http://localhost/database',
                    'icon': 'bi bi-database',
                    'block': 'Dados'
                },
                {
                    'name': 'Sistema de Backup',
                    'url': 'http://localhost/backup',
                    'icon': 'bi bi-shield-lock',
                    'block': 'Administração'
                },
                {
                    'name': 'Portal do Cliente',
                    'url': 'http://localhost/cliente',
                    'icon': 'bi bi-people',
                    'block': 'Clientes'
                },
                {
                    'name': 'Sistema de Licitações',
                    'url': 'http://localhost/licitacoes',
                    'icon': 'bi bi-file-earmark-text',
                    'block': 'Licitações'
                }
            ]

            # Check if links already exist
            existing_count = SystemLink.query.count()
            if existing_count > 0:
                print(f"Já existem {existing_count} links no sistema. Limpando dados existentes...")
                SystemLink.query.delete()
                db.session.commit()

            # Add sample links
            for link_data in sample_links:
                link = SystemLink(
                    name=link_data['name'],
                    url=link_data['url'],
                    icon=link_data['icon'],
                    block=link_data['block']
                )
                db.session.add(link)

            db.session.commit()
            print(f"Adicionados {len(sample_links)} links de exemplo com sucesso!")

            # Show the distinct blocks
            distinct_blocks = db.session.query(SystemLink.block).distinct().all()
            distinct_blocks = [row[0] for row in distinct_blocks if row[0]]

            print(f"\nBlocos criados: {', '.join(distinct_blocks)}")
            print("Agora o dropdown 'Bloco (Opcional)' deve mostrar essas opções!")

        except Exception as e:
            print(f"Erro ao adicionar links de exemplo: {e}")
            db.session.rollback()
            return False

    return True

if __name__ == '__main__':
    success = add_sample_system_links()
    if success:
        print("\nScript executado com sucesso.")
    else:
        print("\nFalha na execução do script.")
        sys.exit(1)
