# servidor_app/services/server_info_service.py
import psutil
import subprocess
import os
from .cache_service import cache

def get_php_version():
    """
    Obtém a versão do PHP instalada.
    """
    php_paths = [
        r"D:\\php\\php.exe",
        r"D:\\xampp\\php\\php.exe",
        "php"  # fallback to system PATH
    ]
    for php_path in php_paths:
        try:
            result = subprocess.run([php_path, '--version'], capture_output=True, text=True, timeout=5, shell=True)
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                if lines:
                    version_line = lines[0]
                    if 'PHP' in version_line:
                        parts = version_line.split()
                        if len(parts) > 1:
                            return parts[1]
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            continue
    return "Não instalado"

def get_mysql_version():
    """
    Obtém a versão do MySQL instalada.
    """
    try:
        result = subprocess.run(['mysql', '--version'], capture_output=True, text=True, timeout=5, shell=True)
        if result.returncode == 0:
            output = result.stdout.strip()
            # Output like: mysql  Ver 8.0.30 for Win64 on x86_64 (MySQL Community Server - GPL)
            if 'Ver' in output:
                parts = output.split('Ver')
                if len(parts) > 1:
                    version = parts[1].split()[0]
                    return version
        return "Não instalado"
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
        return "Não instalado"

def is_xampp_running():
    """
    Verifica se o XAMPP está rodando (Apache e MySQL).
    """
    try:
        apache_running = any(p.info['name'] == 'httpd.exe' for p in psutil.process_iter(['name']))
        mysql_running = any(p.info['name'] == 'mysqld.exe' for p in psutil.process_iter(['name']))
        return apache_running and mysql_running
    except Exception:
        return False

def get_server_info(root_dir):
    """
    Coleta informações de uso de memória e disco com cache.
    """
    cache_key = f"server_info_{root_dir}"

    # Tenta obter do cache primeiro
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data

    # Coleta informações se não estiver em cache
    memory_percent = psutil.virtual_memory().percent
    total_memory_gb = round(psutil.virtual_memory().total / (1024**3), 2)

    try:
        disk_usage = psutil.disk_usage(root_dir)
        disk_percent = disk_usage.percent
        total_disk_gb = round(disk_usage.total / (1024**3), 2)
    except FileNotFoundError:
        # Lida com o caso em que o disco/caminho não existe
        disk_percent = 0
        total_disk_gb = 0

    # Coleta versões de software
    php_version = get_php_version()
    mysql_version = get_mysql_version()
    xampp_running = is_xampp_running()

    data = {
        'memory_percent': memory_percent,
        'total_memory_gb': total_memory_gb,
        'disk_percent': disk_percent,
        'total_disk_gb': total_disk_gb,
        'php_version': php_version,
        'mysql_version': mysql_version,
        'xampp_running': xampp_running
    }

    # Armazena no cache por 60 segundos
    cache.set(cache_key, data, ttl_seconds=60)

    return data
