import time
from typing import Any, Dict, Optional

class SimpleCache:
    """
    Cache simples em memória com expiração de tempo.
    """
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}

    def get(self, key: str) -> Optional[Any]:
        """Obtém um valor do cache se não expirou."""
        if key in self._cache:
            entry = self._cache[key]
            if time.time() < entry['expires_at']:
                return entry['value']
            else:
                del self._cache[key]
        return None

    def set(self, key: str, value: Any, ttl_seconds: int = 300) -> None:
        """Define um valor no cache com tempo de vida."""
        self._cache[key] = {
            'value': value,
            'expires_at': time.time() + ttl_seconds
        }

    def delete(self, key: str) -> None:
        """Remove um valor do cache."""
        if key in self._cache:
            del self._cache[key]

    def clear(self) -> None:
        """Limpa todo o cache."""
        self._cache.clear()

# Instância global do cache
cache = SimpleCache()
