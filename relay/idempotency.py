import time
from typing import Dict, Tuple, Any

class IdempotencyGuard:
    def __init__(self, ttl_seconds: float = 300.0):
        self.ttl_seconds = ttl_seconds
        # key -> (stored_time, response_payload)
        self.cache: Dict[str, Tuple[float, Any]] = {}

    def is_seen(self, idempotency_key: str) -> bool:
        self.purge_expired()
        return idempotency_key in self.cache

    def record(self, idempotency_key: str, response: Any):
        self.cache[idempotency_key] = (time.time(), response)

    def get_cached(self, idempotency_key: str) -> Any:
        if self.is_seen(idempotency_key):
            return self.cache[idempotency_key][1]
        return None

    def purge_expired(self):
        now = time.time()
        expired = [k for k, (t, _) in self.cache.items() if now - t > self.ttl_seconds]
        for k in expired:
            del self.cache[k]
