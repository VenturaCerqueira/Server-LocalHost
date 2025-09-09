# servidor_app/__init__.py

from flask import Flask, request
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import os

# Instanciar o SQLAlchemy e o LoginManager
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'

from servidor_app.services.server_info_service import get_server_info

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('servidor_app.config.Config')

    if test_config:
        app.config.from_mapping(test_config)

    # Add min and max functions to Jinja2 globals
    app.jinja_env.globals.update(min=min, max=max)

    # Inicializar as extensões com a aplicação
    db.init_app(app)
    login_manager.init_app(app)

    # Inicializar otimizadores de performance
    import servidor_app.services.database_service as db_service
    from .services.database_service import DatabaseOptimizer
    from .services.optimization_service import performance_optimizer

    # Otimizador de banco de dados
    db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
    db_service.db_optimizer = DatabaseOptimizer(db_path)

    # Importar os modelos e blueprints após db ser inicializado para evitar o circular import
    from .models.user_model import User
    from .controllers.main_controller import main_bp
    from .controllers.api_controller import api_bp
    from .controllers.git_api import git_api_bp
    from .controllers.file_api import file_api_bp
    from .controllers.sync_api import sync_api_bp
    from .controllers.auth_controller import auth_bp

    # Registrar os Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(git_api_bp)
    app.register_blueprint(file_api_bp)
    app.register_blueprint(sync_api_bp)
    app.register_blueprint(auth_bp)

    # Import metrics service after app creation
    from .services.metrics_service import metrics_service

    @app.before_request
    def before_request():
        metrics_service.start_request()

    @app.after_request
    def after_request(response):
        if hasattr(request, 'endpoint') and request.endpoint:
            endpoint = str(request.endpoint)
            method = request.method
            status_code = response.status_code
            metrics_service.end_request(endpoint, method, status_code)
        return response

    # Cleanup ao fechar aplicação
    @app.teardown_appcontext
    def cleanup_resources(exception=None):
        import servidor_app.services.database_service as db_service
        if hasattr(db_service, 'db_optimizer') and db_service.db_optimizer:
            db_service.db_optimizer.cleanup()
        performance_optimizer.cleanup()

    @app.context_processor
    def inject_dados_servidor():
        try:
            dados_servidor = get_server_info(app.config['ROOT_DIR'])
        except Exception:
            dados_servidor = None
        return dict(dados_servidor=dados_servidor)

    return app

# Adicionar o user loader, que o Flask-Login precisa para carregar os usuários
from .models.user_model import User
from .models.file_metadata_model import FileMetadata

@login_manager.user_loader
def load_user(user_id):
    # Carrega o usuário do banco de dados apenas se estiver ativo
    user = User.query.get(int(user_id))
    if user and user.is_active:
        return user
    return None
