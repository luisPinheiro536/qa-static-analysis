import hashlib
import os
import pickle
from pathlib import Path
from .history import AnalysisHistory
from .logger import StructuredLogger


class AnalysisCache:
    """Cache de análises com invalidação por hash."""

    def __init__(self, cache_dir=".cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def _get_file_hash(self, filepath):
        """Calcula SHA256 do arquivo."""
        sha = hashlib.sha256()
        with open(filepath, 'rb') as f:
            sha.update(f.read())
        return sha.hexdigest()

    def _get_cache_key(self, filepath):
        """Gera chave de cache baseada em arquivo + hash."""
        file_hash = self._get_file_hash(filepath)
        return f"{Path(filepath).stem}_{file_hash}.cache"

    def get(self, filepath):
        """Retorna resultado em cache se válido."""
        cache_key = self._get_cache_key(filepath)
        cache_file = self.cache_dir / cache_key
        
        if cache_file.exists():
            with open(cache_file, 'rb') as f:
                return pickle.load(f)
        return None

    def set(self, filepath, data):
        """Armazena resultado em cache."""
        cache_key = self._get_cache_key(filepath)
        cache_file = self.cache_dir / cache_key
        
        with open(cache_file, 'wb') as f:
            pickle.dump(data, f)

    def clear(self):
        """Limpa todo o cache."""
        import shutil
        shutil.rmtree(self.cache_dir, ignore_errors=True)
        self.cache_dir.mkdir()

    def get_stats(self):
        """Retorna estatísticas do cache."""
        files = list(self.cache_dir.glob("*.cache"))
        return {
            "cache_size": sum(f.stat().st_size for f in files),
            "file_count": len(files)
        }

# Importar logger para fácil acesso
from .logger import StructuredLogger

__all__ = ['AnalysisCache', 'StructuredLogger']