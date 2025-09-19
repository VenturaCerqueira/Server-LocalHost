#!/usr/bin/env python3
"""
Script to update url_for calls in templates after controller reorganization.
"""

import os
import re

def update_template_file(filepath):
    """Update url_for calls in a template file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define the mapping of old to new endpoints
    replacements = {
        "url_for('main.index')": "url_for('file.index')",
        "url_for('main.login')": "url_for('user.login')",
        "url_for('main.register')": "url_for('user.register')",
        "url_for('main.logout')": "url_for('user.logout')",
        "url_for('main.perfil')": "url_for('user.perfil')",
        "url_for('main.configuracoes')": "url_for('user.configuracoes')",
        "url_for('main.admin')": "url_for('admin.admin')",
        "url_for('main.databases')": "url_for('database.databases')",
        "url_for('main.sistemas')": "url_for('system.sistemas')",
        "url_for('main.portal')": "url_for('system.portal')",
        "url_for('main.add_system_link')": "url_for('system.add_system_link')",
        "url_for('main.edit_system_link')": "url_for('system.edit_system_link')",
        "url_for('main.delete_system_link')": "url_for('system.delete_system_link')",
        "url_for('main.licitacoes')": "url_for('system.licitacoes')",
        "url_for('main.dropbox')": "url_for('system.dropbox')",
        "url_for('main.metrics')": "url_for('system.metrics')",
        "url_for('main.performance')": "url_for('system.performance')",
        "url_for('main.dados_pessoais')": "url_for('file.dados_pessoais')",
        "url_for('main.browse')": "url_for('file.browse')",
        "url_for('main.toggle_user')": "url_for('admin.toggle_user')",
        "url_for('main.delete_user')": "url_for('admin.delete_user')",
        "url_for('main.assign_role')": "url_for('admin.assign_role')",
        "url_for('main.admin_roles')": "url_for('admin.admin_roles')",
        "url_for('main.secure_folder_password')": "url_for('file.secure_folder_password')",
        "url_for('main.edit_system_link')": "url_for('system.edit_system_link')",
        "url_for('main.delete_system_link')": "url_for('system.delete_system_link')",
        "url_for('main.sistemas')": "url_for('system.sistemas')",
        "url_for('main.licitacoes')": "url_for('system.licitacoes')",
        "url_for('main.dropbox')": "url_for('system.dropbox')",
    }

    # Apply replacements
    for old, new in replacements.items():
        content = content.replace(old, new)

    # Write back if changed
    with open(filepath, 'r', encoding='utf-8') as f:
        original_content = f.read()

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")
        return True
    return False

def main():
    """Main function to update all template files."""
    templates_dir = 'servidor_app/templates'

    updated_files = []
    for root, dirs, files in os.walk(templates_dir):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                if update_template_file(filepath):
                    updated_files.append(filepath)

    print(f"Updated {len(updated_files)} template files:")
    for f in updated_files:
        print(f"  - {f}")

if __name__ == '__main__':
    main()
