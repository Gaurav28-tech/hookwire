import time
import math
from typing import List, Dict, Optional
from relay.models import WebhookEvent, DeliveryStatus

class RetryQueue:
    def __init__(self, max_retries: int = 3, base_backoff_seconds: float = 1.0, max_backoff_seconds: float = 60.0):
        self.max_retries = max_retries
        self.base_backoff_seconds = base_backoff_seconds
        self.max_backoff_seconds = max_backoff_seconds
        self.active_queue: List[WebhookEvent] = []
        self.dlq: List[WebhookEvent] = []

    def enqueue(self, event: WebhookEvent):
        event.status = DeliveryStatus.PENDING
        event.next_attempt_at = time.time()
        self.active_queue.append(event)

    def calculate_backoff(self, attempts: int) -> float:
        backoff = self.base_backoff_seconds * (2 ** attempts)
        return min(backoff, self.max_backoff_seconds)

    def handle_failure(self, event: WebhookEvent, error_msg: str):
        event.attempts += 1
        event.last_error = error_msg

        if event.attempts >= self.max_retries:
            event.status = DeliveryStatus.DEAD_LETTERED
            self.dlq.append(event)
        else:
            event.status = DeliveryStatus.RETRYING
            delay = self.calculate_backoff(event.attempts)
            event.next_attempt_at = time.time() + delay
            self.active_queue.append(event)

    def handle_success(self, event: WebhookEvent):
        event.status = DeliveryStatus.DELIVERED

    def get_ready_events(self) -> List[WebhookEvent]:
        now = time.time()
        ready = [e for e in self.active_queue if e.next_attempt_at <= now]
        self.active_queue = [e for e in self.active_queue if e.next_attempt_at > now]
        return ready
