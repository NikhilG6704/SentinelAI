"""
Thread-safe in-memory model cache.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from threading import Lock
from typing import Any

from serving.configuration import serving_config


@dataclass
class CachedModel:
    """
    Cached model metadata.
    """

    name: str
    version: str
    stage: str
    model: Any
    loaded_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )


class ModelCache:
    """
    Thread-safe in-memory model cache.
    """

    def __init__(self) -> None:
        self._cache: dict[str, CachedModel] = {}
        self._lock = Lock()

        self._hits = 0
        self._misses = 0

    # ------------------------------------------------------------------
    # Cache Operations
    # ------------------------------------------------------------------

    def get(
        self,
        model_name: str,
    ) -> CachedModel | None:

        with self._lock:

            model = self._cache.get(model_name)

            if model is None:
                self._misses += 1
                return None

            self._hits += 1
            return model

    def put(
        self,
        model_name: str,
        model: Any,
        version: str,
        stage: str,
    ) -> CachedModel:

        with self._lock:

            cached = CachedModel(
                name=model_name,
                version=version,
                stage=stage,
                model=model,
            )

            self._cache[model_name] = cached

            return cached

    def remove(
        self,
        model_name: str,
    ) -> None:

        with self._lock:
            self._cache.pop(model_name, None)

    def clear(self) -> None:

        with self._lock:
            self._cache.clear()

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def contains(
        self,
        model_name: str,
    ) -> bool:

        with self._lock:
            return model_name in self._cache

    def list_models(self) -> list[str]:

        with self._lock:
            return sorted(self._cache.keys())

    def items(self) -> list[CachedModel]:
        """
        Return a snapshot of all cached models.
        """

        with self._lock:
            return list(self._cache.values())

    def size(self) -> int:

        with self._lock:
            return len(self._cache)

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    @property
    def hits(self) -> int:
        return self._hits

    @property
    def misses(self) -> int:
        return self._misses

    @property
    def hit_rate(self) -> float:

        total = self._hits + self._misses

        if total == 0:
            return 0.0

        return self._hits / total

    def stats(self) -> dict[str, Any]:
        """
        Cache statistics for health monitoring.
        """

        return {
            "enabled": serving_config.cache_enabled,
            "size": self.size(),
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": round(self.hit_rate, 3),
            "models": self.list_models(),
        }


model_cache = ModelCache()