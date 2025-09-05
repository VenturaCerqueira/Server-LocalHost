"""
Serviço de Otimizações de Performance
Gerencia pools de threads, conexões e operações otimizadas de I/O
"""
import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Any, Optional
import psutil
import logging

logger = logging.getLogger(__name__)

class PerformanceOptimizer:
    """
    Gerenciador de otimizações de performance para operações de I/O e processamento
    """

    def __init__(self, max_workers: int = None):
        # Define número ótimo de workers baseado no sistema
        if max_workers is None:
            cpu_count = os.cpu_count() or 4
            max_workers = min(cpu_count * 2, 16)  # Máximo 16 workers

        self.executor = ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="file_ops")
        self.file_cache: Dict[str, Dict[str, Any]] = {}
        self.cache_lock = threading.Lock()

        # Métricas de performance
        self.metrics = {
            'file_operations': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'avg_operation_time': 0.0
        }

        logger.info(f"PerformanceOptimizer initialized with {max_workers} workers")

    def get_file_info_batch(self, file_paths: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Obtém informações de múltiplos arquivos em paralelo
        """
        def get_single_file_info(file_path: str) -> tuple:
            try:
                stat = os.stat(file_path)
                return file_path, {
                    'size': stat.st_size,
                    'modified': stat.st_mtime,
                    'created': stat.st_ctime,
                    'is_file': os.path.isfile(file_path),
                    'is_dir': os.path.isdir(file_path)
                }
            except (OSError, PermissionError):
                return file_path, None

        # Submete todas as operações para execução paralela
        futures = [self.executor.submit(get_single_file_info, path) for path in file_paths]

        results = {}
        for future in as_completed(futures):
            file_path, info = future.result()
            results[file_path] = info

        return results

    def calculate_directory_size_optimized(self, directory_path: str) -> int:
        """
        Calcula tamanho de diretório de forma otimizada usando paralelismo
        """
        start_time = time.time()

        if not os.path.exists(directory_path):
            return 0

        total_size = 0
        subdirs = []

        try:
            # Primeiro nível - coleta subdiretórios
            with os.scandir(directory_path) as entries:
                for entry in entries:
                    if entry.is_file():
                        total_size += entry.stat().st_size
                    elif entry.is_dir() and not entry.name.startswith('.'):
                        subdirs.append(entry.path)

            # Processa subdiretórios em paralelo
            if subdirs:
                futures = [self.executor.submit(self._calculate_subdir_size, subdir)
                          for subdir in subdirs]

                for future in as_completed(futures):
                    total_size += future.result()

        except (PermissionError, OSError) as e:
            logger.warning(f"Erro ao calcular tamanho do diretório {directory_path}: {e}")

        operation_time = time.time() - start_time
        self._update_metrics(operation_time)

        return total_size

    def _calculate_subdir_size(self, directory_path: str) -> int:
        """
        Calcula tamanho de um subdiretório recursivamente
        """
        total_size = 0
        try:
            for root, dirs, files in os.walk(directory_path):
                # Remove diretórios ocultos da travessia
                dirs[:] = [d for d in dirs if not d.startswith('.')]

                for file in files:
                    try:
                        file_path = os.path.join(root, file)
                        total_size += os.path.getsize(file_path)
                    except (OSError, PermissionError):
                        continue
        except (PermissionError, OSError):
            pass

        return total_size

    def optimize_file_listing(self, directory_path: str, include_hidden: bool = False) -> List[Dict[str, Any]]:
        """
        Lista arquivos de forma otimizada com informações em lote
        """
        start_time = time.time()

        if not os.path.exists(directory_path):
            return []

        entries = []
        file_paths = []

        try:
            with os.scandir(directory_path) as dir_entries:
                for entry in dir_entries:
                    if not include_hidden and entry.name.startswith('.'):
                        continue

                    entries.append(entry)
                    file_paths.append(entry.path)

            # Obtém informações de todos os arquivos em paralelo
            file_infos = self.get_file_info_batch(file_paths)

            result = []
            for entry in entries:
                info = file_infos.get(entry.path)
                if info:
                    result.append({
                        'name': entry.name,
                        'path': entry.path,
                        'size': info['size'],
                        'modified': info['modified'],
                        'created': info['created'],
                        'is_file': info['is_file'],
                        'is_dir': info['is_dir']
                    })

        except (PermissionError, OSError) as e:
            logger.warning(f"Erro ao listar diretório {directory_path}: {e}")
            return []

        operation_time = time.time() - start_time
        self._update_metrics(operation_time)

        return sorted(result, key=lambda x: x['name'].lower())

    def get_system_resources(self) -> Dict[str, Any]:
        """
        Obtém informações otimizadas sobre recursos do sistema
        """
        try:
            memory = psutil.virtual_memory()
            cpu_percent = psutil.cpu_percent(interval=0.1)

            return {
                'memory_percent': memory.percent,
                'memory_used_gb': round(memory.used / (1024**3), 2),
                'memory_total_gb': round(memory.total / (1024**3), 2),
                'cpu_percent': cpu_percent,
                'cpu_count': psutil.cpu_count(),
                'cpu_count_logical': psutil.cpu_count(logical=True)
            }
        except Exception as e:
            logger.error(f"Erro ao obter recursos do sistema: {e}")
            return {}

    def _update_metrics(self, operation_time: float):
        """Atualiza métricas de performance"""
        with self.cache_lock:
            self.metrics['file_operations'] += 1
            self.metrics['avg_operation_time'] = (
                (self.metrics['avg_operation_time'] * (self.metrics['file_operations'] - 1)) +
                operation_time
            ) / self.metrics['file_operations']

    def get_performance_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas de performance"""
        return {
            'file_operations': self.metrics['file_operations'],
            'cache_hits': self.metrics['cache_hits'],
            'cache_misses': self.metrics['cache_misses'],
            'avg_operation_time': round(self.metrics['avg_operation_time'], 4),
            'active_threads': threading.active_count(),
            'executor_workers': self.executor._max_workers
        }

    def cleanup(self):
        """Limpa recursos"""
        self.executor.shutdown(wait=True)
        with self.cache_lock:
            self.file_cache.clear()

# Instância global do otimizador
performance_optimizer = PerformanceOptimizer()
