# servidor_app/config.py

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Kinfo2013'
    
    # Configuração do banco de dados SQLite para uso local da aplicação
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Diretório raiz para a aplicação local
    ROOT_DIR = 'D:/Servidor/'
    
    # Configurações para uploads
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip'}
    
    # --- Configurações Adicionadas para Gerenciamento de Banco de Dados ---
    
    # Diretório local onde os bancos de dados do XAMPP estão armazenados
    DB_ROOT_DIR = 'D:/Servidor/xampp/mysql/data' # CAMINHO CORRIGIDO
    
    # Novo diretório para listar os sistemas
    SISTEMAS_DIR = 'D:/Servidor/xampp/htdocs'
    
    # Credenciais do banco de dados de produção
    PROD_DB_HOST = 'db-keepsistemas-sql8.c3emmyqhonte.sa-east-1.rds.amazonaws.com'
    PROD_DB_USER = os.environ.get('PROD_DB_USER') or 'anderson'
    PROD_DB_PASSWORD = os.environ.get('PROD_DB_PASSWORD') or '126303@acv'
    PROD_DB_PORT = os.environ.get('PROD_DB_PORT') or 3306