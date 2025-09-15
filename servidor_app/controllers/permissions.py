from flask import flash, redirect, url_for
from flask_login import current_user
import json

def has_access(area):
    """
    Check if current user has access to a specific area.
    """
    if not current_user.is_authenticated:
        return False

    # Admin user 'keep' has access to everything
    if current_user.username == 'keep':
        return True

    # If user has no role, deny access
    if not current_user.role:
        return False

    # Parse allowed areas from JSON
    try:
        allowed_areas = json.loads(current_user.role.allowed_areas)
    except (json.JSONDecodeError, AttributeError):
        return False

    return area in allowed_areas

def require_access(area):
    """
    Decorator to require access to a specific area.
    """
    def decorator(f):
        def wrapper(*args, **kwargs):
            if not has_access(area):
                flash('Acesso negado. Você não tem permissão para acessar esta área.', 'danger')
                return redirect(url_for('main.index'))
            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator

# Define area constants
AREAS = {
    'meus_arquivos': 'meus_arquivos',
    'dados_pessoais': 'dados_pessoais',
    'banco_dados': 'banco_dados',
    'sistemas': 'sistemas',
    'licitacoes': 'licitacoes',
    'dropbox': 'dropbox',
    'metrics': 'metrics',
    'performance': 'performance',
    'admin': 'admin'
}
