from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Dict, Any
import time

class DeliveryStatus(Enum):
    PENDING = "PENDING"
    DELIVERED = "DELIVERED"
    RETRYING = "RETRYING"
    DEAD_LETTERED = "DEAD_LETTERED"

@dataclass
class WebhookEvent:
    id: str
    target_url: str
    payload: str
    headers: Dict[str, str] = field(default_factory=dict)
    attempts: int = 0
    max_retries: int = 3
    next_attempt_at: float = field(default_factory=time.time)
    status: DeliveryStatus = DeliveryStatus.PENDING
    last_error: Optional[str] = None
