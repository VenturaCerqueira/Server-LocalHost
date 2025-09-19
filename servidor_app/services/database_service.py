"""
Serviço de Otimização de Banco de Dados
Gerencia conexões, queries otimizadas e pool de conexões
"""
import sqlite3
import threading
import time
import logging
import os
import subprocess
import tempfile
import re
from typing import Dict, List, Any, Optional, Tuple
from contextlib import contextmanager
import pymysql

logger = logging.getLogger(__name__)

class DatabaseOptimizer:
    """
    Otimizador de banco de dados com pool de conexões e queries otimizadas
    """

    def __init__(self, db_path: str, max_connections: int = 5):
        self.db_path = db_path
        self.max_connections = max_connections
        self._connection_pool: List[sqlite3.Connection] = []
        self._pool_lock = threading.Lock()
        self._connection_count = 0

        # Cache de queries preparadas
        self._prepared_statements: Dict[str, sqlite3.Statement] = {}

        # Métricas
        self.metrics = {
            'connections_created': 0,
            'connections_reused': 0,
            'queries_executed': 0,
            'avg_query_time': 0.0
        }

        # Inicializa pool de conexões
        self._initialize_pool()

        logger.info(f"DatabaseOptimizer initialized with pool size {max_connections}")

    def _initialize_pool(self):
        """Inicializa o pool de conexões"""
        for _ in range(self.max_connections):
            conn = self._create_connection()
            self._connection_pool.append(conn)

    def _create_connection(self) -> sqlite3.Connection:
        """Cria uma nova conexão otimizada"""
        conn = sqlite3.connect(
            self.db_path,
            check_same_thread=False,  # Permite uso em threads diferentes
            timeout=30.0
        )

        # Configurações de performance
        conn.execute("PRAGMA journal_mode=WAL")  # Write-Ahead Logging
        conn.execute("PRAGMA synchronous=NORMAL")  # Balance entre velocidade e segurança
        conn.execute("PRAGMA cache_size=-64000")  # 64MB cache
        conn.execute("PRAGMA temp_store=MEMORY")  # Armazenamento temporário em memória
        conn.execute("PRAGMA mmap_size=268435456")  # 256MB memory-mapped I/O

        # Cria índices se não existirem
        self._create_optimized_indexes(conn)

        self.metrics['connections_created'] += 1
        return conn

    def _create_optimized_indexes(self, conn: sqlite3.Connection):
        """Cria índices otimizados para melhor performance"""
        try:
            # Índice para usuários por username (login frequente)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_users_username
                ON user(username)
            """)

            # Note: Email column doesn't exist in user table, so we skip this index
            # If email column is added later, this index can be re-enabled
            pass

            conn.commit()
        except sqlite3.Error as e:
            logger.warning(f"Erro ao criar índices: {e}")

    @contextmanager
    def get_connection(self):
        """Obtém uma conexão do pool de forma thread-safe"""
        conn = None
        try:
            with self._pool_lock:
                if self._connection_pool:
                    conn = self._connection_pool.pop()
                    self.metrics['connections_reused'] += 1
                else:
                    # Cria nova conexão se pool estiver vazio
                    conn = self._create_connection()

            yield conn

        finally:
            if conn:
                with self._pool_lock:
                    if len(self._connection_pool) < self.max_connections:
                        self._connection_pool.append(conn)
                    else:
                        conn.close()

    def execute_query(self, query: str, params: Tuple = None, fetch: bool = True) -> List[Dict[str, Any]]:
        """
        Executa query de forma otimizada com métricas
        """
        start_time = time.time()

        with self.get_connection() as conn:
            try:
                cursor = conn.cursor()

                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)

                if fetch and cursor.description:
                    columns = [desc[0] for desc in cursor.description]
                    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
                else:
                    results = []

                conn.commit()

                # Atualiza métricas
                query_time = time.time() - start_time
                self._update_query_metrics(query_time)

                return results

            except sqlite3.Error as e:
                logger.error(f"Erro na query '{query}': {e}")
                conn.rollback()
                raise

    def execute_batch(self, queries: List[Tuple[str, Tuple]]) -> bool:
        """
        Executa múltiplas queries em lote para melhor performance
        """
        start_time = time.time()

        with self.get_connection() as conn:
            try:
                cursor = conn.cursor()

                for query, params in queries:
                    if params:
                        cursor.execute(query, params)
                    else:
                        cursor.execute(query)

                conn.commit()

                # Atualiza métricas
                batch_time = time.time() - start_time
                avg_time = batch_time / len(queries)
                self._update_query_metrics(avg_time, len(queries))

                return True

            except sqlite3.Error as e:
                logger.error(f"Erro no lote de queries: {e}")
                conn.rollback()
                return False

    def _update_query_metrics(self, query_time: float, count: int = 1):
        """Atualiza métricas de queries"""
        self.metrics['queries_executed'] += count
        self.metrics['avg_query_time'] = (
            (self.metrics['avg_query_time'] * (self.metrics['queries_executed'] - count)) +
            (query_time * count)
        ) / self.metrics['queries_executed']

    def get_database_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do banco de dados"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                # Estatísticas da tabela de usuários
                cursor.execute("SELECT COUNT(*) as user_count FROM user")
                user_count = cursor.fetchone()[0]

                # Tamanho do arquivo de banco
                db_size = os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0

                return {
                    'user_count': user_count,
                    'db_size_mb': round(db_size / (1024 * 1024), 2),
                    'connections_created': self.metrics['connections_created'],
                    'connections_reused': self.metrics['connections_reused'],
                    'queries_executed': self.metrics['queries_executed'],
                    'avg_query_time': round(self.metrics['avg_query_time'], 4),
                    'pool_size': len(self._connection_pool)
                }

        except Exception as e:
            logger.error(f"Erro ao obter estatísticas do banco: {e}")
            return {}

    def optimize_database(self) -> Dict[str, str]:
        """
        Executa otimizações no banco de dados
        """
        results = {}

        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                # Reindexa tabelas
                cursor.execute("REINDEX")
                results['reindex'] = "Reindexação concluída"

                # Otimiza banco
                cursor.execute("VACUUM")
                results['vacuum'] = "Otimização concluída"

                # Analisa estatísticas para otimizador de queries
                cursor.execute("ANALYZE")
                results['analyze'] = "Análise de estatísticas concluída"

                conn.commit()

        except sqlite3.Error as e:
            results['error'] = f"Erro na otimização: {e}"

        return results

    def cleanup(self):
        """Limpa recursos do pool de conexões"""
        with self._pool_lock:
            for conn in self._connection_pool:
                try:
                    conn.close()
                except:
                    pass
            self._connection_pool.clear()

def list_local_mysql_databases(config) -> Dict[str, Any]:
    """
    Lista bancos de dados MySQL locais (XAMPP)
    """
    local_user = 'root'
    local_password = ''

    try:
        # Caminho completo para o executável MySQL do XAMPP
        mysql_path = r'D:\Servidor\xampp\mysql\bin\mysql.exe'

        # Comando para listar bancos
        cmd = [
            mysql_path,
            '-u', local_user,
            f'-p{local_password}' if local_password else '',
            '-e', 'SHOW DATABASES;'
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            error_msg = result.stderr.strip()
            logger.error(f"Erro ao listar bancos locais: {error_msg}")
            return {
                'success': False,
                'error': f'Falha ao listar bancos locais: {error_msg}',
                'databases': []
            }

        # Parse output - skip header and system databases
        lines = result.stdout.strip().split('\n')[1:]  # Skip header
        databases = []
        system_dbs = {'information_schema', 'mysql', 'performance_schema', 'sys', 'phpmyadmin'}

        for line in lines:
            db_name = line.strip()
            if db_name and db_name not in system_dbs:
                databases.append(db_name)

        return {
            'success': True,
            'databases': databases,
            'count': len(databases)
        }

    except Exception as e:
        logger.error(f"Erro ao listar bancos locais: {str(e)}")
        return {
            'success': False,
            'error': f'Erro inesperado: {str(e)}',
            'databases': []
        }

def list_production_mysql_databases(config) -> Dict[str, Any]:
    """
    Lista bancos de dados MySQL de produção usando pymysql
    """
    prod_host = config.get('PROD_DB_HOST', 'db-keepsistemas-sql8.c3emmyqhonte.sa-east-1.rds.amazonaws.com')
    prod_port = config.get('PROD_DB_PORT', 3306)
    prod_user = config.get('PROD_DB_USER', 'servidor')
    prod_password = config.get('PROD_DB_PASSWORD', 'servkinfo2013')

    connection = None
    try:
        logger.info(f"Conectando ao banco de produção: {prod_host}:{prod_port}")

        # Conecta ao servidor MySQL sem especificar um banco de dados
        connection = pymysql.connect(
            host=prod_host,
            port=prod_port,
            user=prod_user,
            password=prod_password,
            cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=15,
            read_timeout=300,
            write_timeout=300
        )

        logger.info("Conectado com sucesso ao servidor MySQL de produção")

        with connection.cursor() as cursor:
            # Lista todos os bancos de dados
            cursor.execute("SHOW DATABASES;")
            result = cursor.fetchall()

        # Extrai os nomes dos bancos e filtra bancos do sistema
        databases = []
        system_dbs = {'information_schema', 'mysql', 'performance_schema', 'sys'}

        for row in result:
            db_name = row['Database']
            if db_name and db_name not in system_dbs:
                databases.append(db_name)

        logger.info(f"Encontrados {len(databases)} bancos de dados de produção")
        return {
            'success': True,
            'databases': databases,
            'count': len(databases)
        }

    except pymysql.MySQLError as e:
        error_msg = str(e)
        logger.error(f"Erro MySQL ao listar bancos de produção: {error_msg}")

        # Trata erro de acesso negado especificamente
        if e.args[0] == 1045:  # Access denied
            return {
                'success': False,
                'error': f'Acesso negado ao servidor MySQL de produção. Verifique as credenciais e permissões.',
                'details': error_msg,
                'suggestion': f'Adicione o IP atual ao Security Group do RDS no AWS Console ou verifique as permissões do usuário "{prod_user}".'
            }

        return {
            'success': False,
            'error': f'Erro de conexão MySQL: {error_msg}',
            'databases': []
        }

    except Exception as e:
        error_msg = str(e)
        logger.error(f"Erro inesperado ao listar bancos de produção: {error_msg}")
        return {
            'success': False,
            'error': f'Erro inesperado: {error_msg}',
            'databases': []
        }

    finally:
        if connection and connection.open:
            connection.close()
            logger.info("Conexão com o servidor MySQL de produção encerrada")

def sync_mysql_production_to_local(db_name: str, config) -> Dict[str, Any]:
    """
    Sincroniza banco de dados MySQL da produção para localhost (XAMPP)
    """
    # Credenciais de produção
    prod_host = config.get('PROD_DB_HOST')
    prod_user = config.get('PROD_DB_USER')
    prod_password = config.get('PROD_DB_PASSWORD')
    prod_port = config.get('PROD_DB_PORT', 3306)

    # Credenciais locais (XAMPP padrão)
    local_user = 'root'
    local_password = ''

    if not all([prod_host, prod_user, prod_password]):
        return {
            'success': False,
            'error': 'Credenciais de produção não configuradas'
        }

    # Cria arquivo temporário para o dump
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.sql', delete=False) as temp_file:
        temp_path = temp_file.name

    try:
        logger.info(f"Iniciando sincronização do banco {db_name} da produção para localhost")

        # Comando mysqldump para produção (usando MYSQL_PWD para segurança)
        dump_cmd = [
            'mysqldump',
            '-h', prod_host,
            '-P', str(prod_port),
            '-u', prod_user,
            db_name
        ]

        logger.info(f"Comando dump: {' '.join(dump_cmd)} (usando MYSQL_PWD)")

        # Define MYSQL_PWD no ambiente para evitar passar senha na linha de comando
        env = os.environ.copy()
        env['MYSQL_PWD'] = prod_password

        # Executa dump
        with open(temp_path, 'w') as dump_file:
            result = subprocess.run(
                dump_cmd,
                stdout=dump_file,
                stderr=subprocess.PIPE,
                text=True,
                env=env
            )

        if result.returncode != 0:
            error_msg = result.stderr.strip()
            logger.error(f"Erro no dump: {error_msg}")

            # Verifica se é erro de acesso negado
            if "Access denied" in error_msg:
                return {
                    'success': False,
                    'error': f'Acesso negado ao banco de produção. Verifique as permissões do usuário "{prod_user}" no servidor MySQL.',
                    'details': error_msg,
                    'suggestion': f'Execute no servidor de produção: GRANT ALL PRIVILEGES ON *.* TO \'{prod_user}\'@\'191.195.115.190\' IDENTIFIED BY \'senha\'; FLUSH PRIVILEGES;',
                    'aws_solution': 'Ou adicione o IP atual ao Security Group do RDS no AWS Console: RDS > Databases > db-keepsistemas-sql8 > Connectivity & security > Security group > Add inbound rule (MySQL, TCP, 3306, Source: seu_IP/32)'
                }

            return {
                'success': False,
                'error': f'Falha no dump da produção: {error_msg}'
            }

        logger.info("Dump da produção concluído com sucesso")

        # Comando mysql para restaurar localmente
        restore_cmd = [
            'mysql',
            '-u', local_user,
            f'-p{local_password}' if local_password else '',
            db_name
        ]

        # Executa restore
        with open(temp_path, 'r') as dump_file:
            result = subprocess.run(
                restore_cmd,
                stdin=dump_file,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

        if result.returncode != 0:
            error_msg = result.stderr.strip()
            logger.error(f"Erro na restauração: {error_msg}")
            return {
                'success': False,
                'error': f'Falha na restauração local: {error_msg}'
            }

        logger.info(f"Sincronização do banco {db_name} concluída com sucesso")
        return {
            'success': True,
            'message': f'Banco de dados {db_name} sincronizado com sucesso da produção para localhost'
        }

    except Exception as e:
        logger.error(f"Erro durante sincronização: {str(e)}")
        return {
            'success': False,
            'error': f'Erro inesperado: {str(e)}'
        }

    finally:
        # Remove arquivo temporário
        if os.path.exists(temp_path):
            os.unlink(temp_path)

def dump_production_database(config, db_name: str) -> Dict[str, Any]:
    """
    Faz dump do banco de dados MySQL de produção e retorna o conteúdo SQL
    """
    # Credenciais de produção
    prod_host = config.get('PROD_DB_HOST', 'db-keepsistemas-sql8.c3emmyqhonte.sa-east-1.rds.amazonaws.com')
    prod_port = config.get('PROD_DB_PORT', 3306)
    prod_user = config.get('PROD_DB_USER', 'servidor')
    prod_password = config.get('PROD_DB_PASSWORD', 'servkinfo2013')

    # Since this function is only for production DB dumps, no changes needed for local DBs here.
    # The local MySQL database dump functions are separate and unaffected.

    try:
        logger.info(f"Iniciando dump do banco {db_name} da produção")

        # Comando mysqldump otimizado para permissões limitadas
        dump_cmd = [
            'mysqldump',
            '--force',                    # Continua mesmo com erros
            '--quick',                    # Dump linha por linha
            '--lock-tables=false',        # Não bloqueia tabelas (útil se não tem privilégios LOCK)
            '--no-tablespaces',           # Evita privilégios de tablespace
            '--skip-opt',                 # Desabilita opções padrão problemáticas
            '--set-gtid-purged=OFF',     # Evita problemas com GTID
            '--single-transaction',       # Usa transação única se possível
            '--no-create-db',             # Não tenta criar banco (já existe)
            '-u', prod_user,
            '-h', prod_host,
            '-P', str(prod_port),
            db_name
        ]

        logger.info(f"Executando mysqldump para {db_name} com parâmetros otimizados")

        # Define MYSQL_PWD no ambiente para segurança
        env = os.environ.copy()
        env['MYSQL_PWD'] = prod_password

        # Cria arquivo temporário para o dump
        with tempfile.NamedTemporaryFile(mode='w+b', suffix='.sql', delete=False) as temp_file:
            temp_path = temp_file.name

        try:
            # Executa dump diretamente para arquivo
            with open(temp_path, 'wb') as dump_file:
                result = subprocess.run(
                    dump_cmd,
                    stdout=dump_file,
                    stderr=subprocess.PIPE,
                    env=env,
                    timeout=300  # 5 minutos timeout
                )

            if result.returncode != 0:
                error_msg = result.stderr.decode('utf-8', errors='ignore').strip()
                logger.error(f"Erro no dump: {error_msg}")

                # Trata erros específicos de permissões
                if "Access denied" in error_msg:
                    return {
                        'success': False,
                        'error': f'Acesso negado ao banco de dados "{db_name}".',
                        'details': error_msg,
                        'suggestion': f'Execute no servidor: GRANT ALL PRIVILEGES ON {db_name}.* TO \'{prod_user}\'@\'%\'; FLUSH PRIVILEGES;'
                    }

                # Trata outros erros comuns
                if "GTID" in error_msg:
                    return {
                        'success': False,
                        'error': 'Erro relacionado ao GTID. O banco usa replicação GTID.',
                        'details': error_msg,
                        'suggestion': 'Adicione --set-gtid-purged=OFF ao comando mysqldump ou verifique configuração de replicação.'
                    }

                return {
                    'success': False,
                    'error': f'Falha no dump da produção: {error_msg}',
                    'details': 'Verifique os logs detalhados para mais informações.'
                }

            # Lê o conteúdo do arquivo como bytes
            with open(temp_path, 'rb') as dump_file:
                dump_content = dump_file.read()

            # Verifica se o dump não está vazio
            if len(dump_content) < 100:  # Dump muito pequeno
                logger.warning(f"Dump muito pequeno ({len(dump_content)} bytes) - pode estar incompleto")
                return {
                    'success': False,
                    'error': 'Dump gerado está muito pequeno - pode estar incompleto ou vazio.',
                    'details': dump_content.decode('utf-8', errors='ignore')[:500]
                }

        finally:
            # Remove arquivo temporário
            if os.path.exists(temp_path):
                os.unlink(temp_path)

        timestamp = time.strftime('%Y%m%d_%H%M%S')

        logger.info(f"Dump do banco {db_name} concluído com sucesso ({len(dump_content)} caracteres)")

        return {
            'success': True,
            'dump': dump_content,
            'timestamp': timestamp,
            'db_name': db_name
        }

    except subprocess.TimeoutExpired:
        logger.error(f"Timeout no dump do banco {db_name}")
        return {
            'success': False,
            'error': 'Timeout ao fazer dump do banco de dados (5 minutos)',
            'suggestion': 'O banco pode ser muito grande ou a conexão muito lenta. Tente novamente ou verifique a conectividade.'
        }

    except Exception as e:
        logger.error(f"Erro inesperado no dump: {str(e)}")
        return {
            'success': False,
            'error': f'Erro inesperado: {str(e)}'
        }

def _dump_accessible_tables_only(config, db_name: str, prod_host: str, prod_port: int, prod_user: str, prod_password: str) -> Dict[str, Any]:
    """
    Tenta fazer dump apenas das tabelas que o usuário pode acessar
    """
    try:
        logger.info(f"Tentando dump apenas das tabelas acessíveis para {db_name}")

        # Primeiro, lista as tabelas que o usuário pode acessar
        connection = pymysql.connect(
            host=prod_host,
            port=prod_port,
            user=prod_user,
            password=prod_password,
            database=db_name,
            connect_timeout=15
        )

        accessible_tables = []
        with connection.cursor() as cursor:
            try:
                cursor.execute("SHOW TABLES;")
                tables = cursor.fetchall()

                for table_row in tables:
                    table_name = list(table_row.values())[0]
                    try:
                        # Testa se pode fazer SELECT na tabela
                        cursor.execute(f"SELECT 1 FROM `{table_name}` LIMIT 1;")
                        accessible_tables.append(table_name)
                        logger.info(f"Tabela {table_name}: acessível")
                    except pymysql.MySQLError as e:
                        logger.warning(f"Tabela {table_name}: não acessível - {str(e)}")
                        continue

            except pymysql.MySQLError as e:
                logger.error(f"Erro ao listar tabelas: {str(e)}")
                return {
                    'success': False,
                    'error': 'Não foi possível listar as tabelas do banco.',
                    'details': str(e)
                }

        connection.close()

        if not accessible_tables:
            return {
                'success': False,
                'error': f'Nenhuma tabela acessível encontrada no banco "{db_name}".',
                'details': f'Usuário "{prod_user}" não tem permissões SELECT em nenhuma tabela.'
            }

        logger.info(f"Tabelas acessíveis encontradas: {len(accessible_tables)}")

        # Faz dump apenas das tabelas acessíveis
        dump_cmd = [
            'mysqldump',
            '--force',
            '--quick',
            '--lock-tables=false',
            '--no-tablespaces',
            '--skip-opt',
            '--set-gtid-purged=OFF',
            '--no-create-db',
            '-u', prod_user,
            '-h', prod_host,
            '-P', str(prod_port),
            db_name
        ] + accessible_tables  # Adiciona apenas as tabelas acessíveis

        logger.info(f"Executando mysqldump apenas para tabelas acessíveis: {accessible_tables}")

        env = os.environ.copy()
        env['MYSQL_PWD'] = prod_password

        with tempfile.NamedTemporaryFile(mode='w+b', suffix='.sql', delete=False) as temp_file:
            temp_path = temp_file.name

        try:
            with open(temp_path, 'wb') as dump_file:
                result = subprocess.run(
                    dump_cmd,
                    stdout=dump_file,
                    stderr=subprocess.PIPE,
                    env=env,
                    timeout=300
                )

            if result.returncode != 0:
                error_msg = result.stderr.decode('utf-8', errors='ignore').strip()
                logger.error(f"Erro no dump parcial: {error_msg}")
                return {
                    'success': False,
                    'error': f'Falha no dump parcial das tabelas acessíveis: {error_msg}',
                    'details': f'Tabelas que tentaram acessar: {", ".join(accessible_tables)}'
                }

            with open(temp_path, 'rb') as dump_file:
                dump_content = dump_file.read()

        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

        timestamp = time.strftime('%Y%m%d_%H%M%S')

        logger.info(f"Dump parcial concluído com sucesso ({len(dump_content)} caracteres, {len(accessible_tables)} tabelas)")

        return {
            'success': True,
            'dump': dump_content,
            'timestamp': timestamp,
            'db_name': db_name,
            'partial_dump': True,
            'accessible_tables': accessible_tables,
            'message': f'Dump parcial realizado com {len(accessible_tables)} tabelas acessíveis.'
        }

    except Exception as e:
        logger.error(f"Erro no dump parcial: {str(e)}")
        return {
            'success': False,
            'error': f'Erro no dump parcial: {str(e)}'
        }

# Instância global será criada no app initialization
db_optimizer = None

def get_local_mysql_connection(config, database=None):
    """
    Retorna uma conexão pymysql para o banco MySQL local (XAMPP) usando as configurações do app
    """
    local_host = config.get('LOCAL_DB_HOST', 'localhost')
    local_port = int(config.get('LOCAL_DB_PORT', 3306))
    local_user = config.get('LOCAL_DB_USER', 'root')
    local_password = config.get('LOCAL_DB_PASSWORD', '')

    conn_params = dict(
        host=local_host,
        port=local_port,
        user=local_user,
        password=local_password,
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=int(config.get('MYSQL_CONNECT_TIMEOUT', 15)),
        read_timeout=int(config.get('MYSQL_READ_TIMEOUT', 300)),
        write_timeout=int(config.get('MYSQL_WRITE_TIMEOUT', 300))
    )
    if database:
        conn_params['database'] = database

    connection = pymysql.connect(**conn_params)
    return connection

def get_production_mysql_connection(config, database=None):
    """
    Retorna uma conexão pymysql para o banco de produção usando as configurações do app
    """
    prod_host = config.get('PROD_DB_HOST', 'db-keepsistemas-sql8.c3emmyqhonte.sa-east-1.rds.amazonaws.com')
    prod_port = int(config.get('PROD_DB_PORT', 3306))
    prod_user = config.get('PROD_DB_USER', 'servidor')
    prod_password = config.get('PROD_DB_PASSWORD', 'servkinfo2013')

    conn_params = dict(
        host=prod_host,
        port=prod_port,
        user=prod_user,
        password=prod_password,
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=int(config.get('MYSQL_CONNECT_TIMEOUT', 15)),
        read_timeout=int(config.get('MYSQL_READ_TIMEOUT', 300)),
        write_timeout=int(config.get('MYSQL_WRITE_TIMEOUT', 300))
    )
    if database:
        conn_params['database'] = database

    connection = pymysql.connect(**conn_params)
    return connection

def delete_local_mysql_database(db_name: str, config) -> Dict[str, Any]:
    """
    Deleta um banco de dados MySQL local (XAMPP)
    """
    local_user = 'root'
    local_password = ''

    try:
        # Caminho completo para o executável MySQL do XAMPP
        mysql_path = r'D:\Servidor\xampp\mysql\bin\mysql.exe'

        # Comando para deletar banco
        cmd = [
            mysql_path,
            '-u', local_user,
            f'-p{local_password}' if local_password else '',
            '-e', f'DROP DATABASE IF EXISTS {db_name};'
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            error_msg = result.stderr.strip()
            logger.error(f"Erro ao deletar banco local {db_name}: {error_msg}")
            return {
                'success': False,
                'error': f'Falha ao deletar banco local: {error_msg}'
            }

        logger.info(f"Banco de dados local {db_name} deletado com sucesso")
        return {
            'success': True,
            'message': f'Banco de dados {db_name} deletado com sucesso'
        }

    except Exception as e:
        logger.error(f"Erro ao deletar banco local {db_name}: {str(e)}")
        return {
            'success': False,
            'error': f'Erro inesperado: {str(e)}'
        }

def analyze_sql_file(sql_file_path: str) -> Dict[str, Any]:
    """
    Analisa arquivo SQL para identificar erros potenciais e problemas
    """
    issues = {
        'errors': [],
        'warnings': [],
        'info': []
    }

    try:
        with open(sql_file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Verificar se o arquivo está vazio
        if not content.strip():
            issues['errors'].append("Arquivo SQL está vazio")
            return issues

        # Dividir em statements SQL (básico)
        statements = []
        current_statement = ""
        in_string = False
        string_char = None
        in_comment = False

        i = 0
        while i < len(content):
            char = content[i]

            if in_comment:
                if char == '\n':
                    in_comment = False
                i += 1
                continue

            if char == '#' or (char == '-' and i + 1 < len(content) and content[i + 1] == '-'):
                in_comment = True
                i += 1
                continue

            if not in_string:
                if char in ('"', "'"):
                    in_string = True
                    string_char = char
                elif char == ';':
                    if current_statement.strip():
                        statements.append(current_statement.strip())
                        current_statement = ""
                    i += 1
                    continue
            else:
                if char == string_char and (i == 0 or content[i - 1] != '\\'):
                    in_string = False
                    string_char = None

            current_statement += char
            i += 1

        # Adicionar último statement se não terminar com ;
        if current_statement.strip():
            statements.append(current_statement.strip())

        # Analisar statements
        tables_created = set()
        tables_referenced = set()
        foreign_keys = []

        for stmt in statements:
            stmt_upper = stmt.upper().strip()

            # Ignorar comentários e statements vazios
            if not stmt_upper or stmt_upper.startswith('--') or stmt_upper.startswith('#'):
                continue

            # Verificar CREATE TABLE
            if stmt_upper.startswith('CREATE TABLE'):
                try:
                    # Extrair nome da tabela
                    table_match = re.search(r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?[`"]?(\w+)[`"]?', stmt_upper, re.IGNORECASE)
                    if table_match:
                        table_name = table_match.group(1)
                        tables_created.add(table_name)

                        # Verificar estrutura básica da tabela
                        if '(' not in stmt or ')' not in stmt:
                            issues['errors'].append(f"Tabela '{table_name}': Sintaxe CREATE TABLE inválida - parênteses ausentes")
                        else:
                            # Verificar colunas
                            columns_part = stmt[stmt.find('(')+1:stmt.rfind(')')]
                            columns = [col.strip() for col in columns_part.split(',') if col.strip()]

                            if not columns:
                                issues['warnings'].append(f"Tabela '{table_name}': Nenhuma coluna definida")

                            for col in columns:
                                col_upper = col.upper()
                                # Verificar PRIMARY KEY
                                if 'PRIMARY KEY' in col_upper:
                                    if not re.search(r'\w+', col.split('PRIMARY KEY')[0].strip()):
                                        issues['warnings'].append(f"Tabela '{table_name}': PRIMARY KEY sem nome de coluna")

                                # Verificar FOREIGN KEY
                                if 'REFERENCES' in col_upper:
                                    fk_match = re.search(r'REFERENCES\s+[`"]?(\w+)[`"]?', col_upper, re.IGNORECASE)
                                    if fk_match:
                                        ref_table = fk_match.group(1)
                                        tables_referenced.add(ref_table)
                                        foreign_keys.append((table_name, ref_table))

                except Exception as e:
                    issues['errors'].append(f"Erro ao analisar CREATE TABLE: {str(e)}")

            # Verificar INSERT INTO
            elif stmt_upper.startswith('INSERT INTO'):
                try:
                    insert_match = re.search(r'INSERT\s+INTO\s+[`"]?(\w+)[`"]?', stmt_upper, re.IGNORECASE)
                    if insert_match:
                        table_name = insert_match.group(1)
                        tables_referenced.add(table_name)

                        # Verificar se VALUES está presente
                        if 'VALUES' not in stmt_upper:
                            issues['warnings'].append(f"INSERT INTO '{table_name}': Statement VALUES ausente")

                except Exception as e:
                    issues['warnings'].append(f"Erro ao analisar INSERT INTO: {str(e)}")

            # Verificar DROP TABLE
            elif stmt_upper.startswith('DROP TABLE'):
                try:
                    drop_match = re.search(r'DROP\s+TABLE\s+(?:IF\s+EXISTS\s+)?[`"]?(\w+)[`"]?', stmt_upper, re.IGNORECASE)
                    if drop_match:
                        table_name = drop_match.group(1)
                        issues['warnings'].append(f"DROP TABLE '{table_name}': Statement de exclusão de tabela encontrado")

                except Exception as e:
                    issues['warnings'].append(f"Erro ao analisar DROP TABLE: {str(e)}")

        # Verificar referências de tabelas
        missing_tables = tables_referenced - tables_created
        if missing_tables:
            for table in missing_tables:
                issues['warnings'].append(f"Tabela '{table}' é referenciada mas não foi criada no dump")

        # Verificar foreign keys para tabelas inexistentes
        for source_table, ref_table in foreign_keys:
            if ref_table not in tables_created:
                issues['warnings'].append(f"Foreign key em '{source_table}' referencia tabela inexistente '{ref_table}'")

        # Estatísticas gerais
        issues['info'].append(f"Total de statements SQL analisados: {len(statements)}")
        issues['info'].append(f"Tabelas criadas: {len(tables_created)}")
        issues['info'].append(f"Tabelas referenciadas: {len(tables_referenced)}")

        if tables_created:
            issues['info'].append(f"Tabelas encontradas: {', '.join(sorted(tables_created))}")

        return issues

    except Exception as e:
        issues['errors'].append(f"Erro geral na análise: {str(e)}")
        return issues

def import_sql_file_to_mysql(sql_file_path: str, db_name: str, config) -> Dict[str, Any]:
    """
    Importa arquivo SQL para banco de dados MySQL local (XAMPP)
    """
    local_user = 'root'
    local_password = ''

    try:
        logger.info(f"Iniciando importação do arquivo {sql_file_path} para o banco {db_name}")

        # Primeiro, analisar o arquivo SQL
        logger.info("Analisando arquivo SQL...")
        analysis_result = analyze_sql_file(sql_file_path)

        # Caminho completo para o executável MySQL do XAMPP
        mysql_path = r'D:\Servidor\xampp\mysql\bin\mysql.exe'

        # Primeiro, criar o banco se não existir
        create_db_cmd = [
            mysql_path,
            '-u', local_user,
            f'-p{local_password}' if local_password else '',
            '-e', f'CREATE DATABASE IF NOT EXISTS {db_name};'
        ]

        logger.info("Criando banco de dados se não existir...")
        create_result = subprocess.run(
            create_db_cmd,
            capture_output=True,
            text=True
        )

        if create_result.returncode != 0:
            error_msg = create_result.stderr.strip()
            logger.error(f"Erro ao criar banco: {error_msg}")
            return {
                'success': False,
                'error': f'Falha ao criar banco de dados: {error_msg}',
                'analysis': analysis_result
            }

        logger.info(f"Banco de dados {db_name} criado/verificado com sucesso")

        # Comando para importar o arquivo SQL
        import_cmd = [
            mysql_path,
            '-u', local_user,
            f'-p{local_password}' if local_password else '',
            db_name
        ]

        logger.info(f"Executando importação do arquivo SQL...")

        # Executar importação com o arquivo SQL
        with open(sql_file_path, 'r', encoding='utf-8', errors='ignore') as sql_file:
            result = subprocess.run(
                import_cmd,
                stdin=sql_file,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

        if result.returncode != 0:
            error_msg = result.stderr.strip()
            logger.error(f"Erro na importação: {error_msg}")
            # Add detailed error logging to a file for debugging
            error_log_path = os.path.join(os.path.dirname(sql_file_path), 'import_error.log')
            with open(error_log_path, 'w', encoding='utf-8') as f:
                f.write(error_msg)
            return {
                'success': False,
                'error': f'Falha na importação: {error_msg}. Veja o arquivo de log: {error_log_path}',
                'analysis': analysis_result
            }

        logger.info(f"Importação do arquivo SQL para {db_name} concluída com sucesso")
        return {
            'success': True,
            'message': f'Arquivo SQL importado com sucesso para o banco {db_name}',
            'analysis': analysis_result
        }

    except FileNotFoundError:
        logger.error(f"Arquivo SQL não encontrado: {sql_file_path}")
        return {
            'success': False,
            'error': f'Arquivo SQL não encontrado: {sql_file_path}',
            'analysis': {'errors': ['Arquivo não encontrado'], 'warnings': [], 'info': []}
        }

    except UnicodeDecodeError as e:
        logger.error(f"Erro de codificação no arquivo SQL: {str(e)}")
        return {
            'success': False,
            'error': f'Erro de codificação no arquivo SQL. Tente salvar o arquivo com codificação UTF-8.',
            'analysis': {'errors': [f'Erro de codificação: {str(e)}'], 'warnings': [], 'info': []}
        }

    except Exception as e:
        logger.error(f"Erro inesperado na importação: {str(e)}")
        return {
            'success': False,
            'error': f'Erro inesperado: {str(e)}',
            'analysis': {'errors': [f'Erro inesperado: {str(e)}'], 'warnings': [], 'info': []}
        }

# Debug log para verificar se o módulo foi carregado corretamente
logger.info("database_service module loaded, dump_production_database function available: %s", hasattr(__import__('__main__'), 'dump_production_database') or 'dump_production_database' in globals())
