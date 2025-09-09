# servidor_app/config.py

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # SECRET_KEY - Gera uma chave aleatória se não fornecida (apenas para desenvolvimento)
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        import secrets
        SECRET_KEY = secrets.token_hex(32)
        print("AVISO: SECRET_KEY não definida. Usando chave aleatória para desenvolvimento.")
        print("IMPORTANTE: Defina SECRET_KEY no arquivo .env para produção!")

    # Configuração do banco de dados SQLite para uso local da aplicação
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Diretório raiz para a aplicação local
    ROOT_DIR = os.environ.get('ROOT_DIR') or 'D:/Servidor/'

    # Configurações para uploads
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip'}

    # --- Configurações Adicionadas para Gerenciamento de Banco de Dados ---

    # Diretório local onde os bancos de dados do XAMPP estão armazenados
    DB_ROOT_DIR = os.environ.get('DB_ROOT_DIR') or 'D:/Servidor/xampp/mysql/data'

    # Novo diretório para listar os sistemas
    SISTEMAS_DIR = os.environ.get('SISTEMAS_DIR') or 'D:/Servidor/xampp/htdocs'

    # Diretório para licitações
    LICITACOES_DIR = os.environ.get('LICITACOES_DIR') or 'D:/Servidor/Licitações'

    # Diretório para Dropbox
    DROPBOX_DIR = os.environ.get('DROPBOX_DIR') or r'C:\Users\desen\Dropbox'

    # Credenciais do banco de dados de produção
    # Para desenvolvimento, permite valores vazios com aviso
    PROD_DB_HOST = os.environ.get('PROD_DB_HOST') or 'db-keepsistemas-sql8.c3emmyqhonte.sa-east-1.rds.amazonaws.com'
    PROD_DB_USER = os.environ.get('PROD_DB_USER') or 'anderson'
    PROD_DB_PASSWORD = os.environ.get('PROD_DB_PASSWORD') or '126303@Acv'
    PROD_DB_PORT = os.environ.get('PROD_DB_PORT') or 3306

    # Validação das credenciais críticas apenas se pelo menos uma estiver definida
    prod_creds_defined = any([PROD_DB_HOST, PROD_DB_USER, PROD_DB_PASSWORD])
    if prod_creds_defined and not all([PROD_DB_HOST, PROD_DB_USER, PROD_DB_PASSWORD]):
        raise ValueError("Se qualquer credencial de produção for definida, todas devem ser fornecidas: PROD_DB_HOST, PROD_DB_USER, PROD_DB_PASSWORD")
    elif not prod_creds_defined:
        print("AVISO: Credenciais de banco de produção não definidas. Funcionalidades de banco estarão limitadas.")

    # Validação adicional para configurações críticas
    if not os.path.exists(ROOT_DIR):
        print(f"AVISO: O diretório raiz '{ROOT_DIR}' não existe. Verifique a configuração ROOT_DIR.")

    if not os.path.exists(DB_ROOT_DIR):
        print(f"AVISO: O diretório de bancos de dados '{DB_ROOT_DIR}' não existe. Funcionalidades de banco estarão limitadas.")

    if not os.path.exists(SISTEMAS_DIR):
        print(f"AVISO: O diretório de sistemas '{SISTEMAS_DIR}' não existe. Funcionalidades de sistemas estarão limitadas.")

    if not os.path.exists(LICITACOES_DIR):
        print(f"AVISO: O diretório de licitações '{LICITACOES_DIR}' não existe. Funcionalidades de licitações estarão limitadas.")

    # Validação de porta do banco de dados
    try:
        PROD_DB_PORT = int(PROD_DB_PORT)
        if PROD_DB_PORT < 1 or PROD_DB_PORT > 65535:
            raise ValueError("Porta inválida")
    except (ValueError, TypeError):
        print("AVISO: PROD_DB_PORT inválida. Usando porta padrão 3306.")
        PROD_DB_PORT = 3306
