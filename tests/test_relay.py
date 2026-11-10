import os
import sys
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from relay.verifier import SignatureVerifier
from relay.idempotency import IdempotencyGuard
from relay.queue import RetryQueue
from relay.models import WebhookEvent, DeliveryStatus

class TestRelayHub(unittest.TestCase):
    def test_signature_verification(self):
        secret = "secret-token-key-123"
        payload = '{"amount": 100, "currency": "USD"}'
        sig = SignatureVerifier.sign(payload, secret)

        self.assertTrue(SignatureVerifier.verify(payload, sig, secret))
        self.assertFalse(SignatureVerifier.verify(payload, "sha256=invalid", secret))
        self.assertFalse(SignatureVerifier.verify('{"amount": 999}', sig, secret))

    def test_idempotency_guard(self):
        guard = IdempotencyGuard(ttl_seconds=10.0)
        key = "req_unique_001"
        self.assertFalse(guard.is_seen(key))

        guard.record(key, {"status": "processed"})
        self.assertTrue(guard.is_seen(key))
        self.assertEqual(guard.get_cached(key), {"status": "processed"})

    def test_retry_queue_and_dlq(self):
        queue = RetryQueue(max_retries=2, base_backoff_seconds=0.1)
        evt = WebhookEvent(id="e1", target_url="https://partner.com", payload="{}")
        
        # 1st failure -> RETRYING
        queue.handle_failure(evt, "Connection timed out")
        self.assertEqual(evt.attempts, 1)
        self.assertEqual(evt.status, DeliveryStatus.RETRYING)
        self.assertEqual(len(queue.dlq), 0)

        # 2nd failure -> DEAD_LETTERED
        queue.handle_failure(evt, "500 Server Error")
        self.assertEqual(evt.attempts, 2)
        self.assertEqual(evt.status, DeliveryStatus.DEAD_LETTERED)
        self.assertEqual(len(queue.dlq), 1)

if __name__ == "__main__":
    unittest.main()
