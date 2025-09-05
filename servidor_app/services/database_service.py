"""
Serviço de Otimização de Banco de Dados
Gerencia conexões, queries otimizadas e pool de conexões
"""
import sqlite3
import threading
import time
import logging
import os
from typing import Dict, List, Any, Optional, Tuple
from contextlib import contextmanager

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

# Instância global será criada no app initialization
db_optimizer = None
