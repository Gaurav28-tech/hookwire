# RelayHub 🔄

[![CI](https://github.com/Gaurav28-tech/relay-hub/actions/workflows/ci.yml/badge.svg)](https://github.com/Gaurav28-tech/relay-hub)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.9+](https://img.shields.io/badge/Python-3.9+-brightgreen.svg)]()

**RelayHub** is a resilient webhook delivery and ingestion pipeline built for high-throughput event-driven microservices. It safeguards webhooks against replay attacks using cryptographic HMAC signatures, enforces idempotent execution, and guarantees at-least-once delivery with exponential backoff and Dead-Letter Queue (DLQ) support.

---

## 🚀 Key Features

- **HMAC-SHA256 Signatures**: Generates and verifies cryptographic signatures with constant-time comparison to prevent timing and spoofing attacks.
- **Idempotency Guard**: Sliding TTL memory store ensuring incoming duplicate webhook deliveries are rejected safely.
- **Exponential Backoff & Jitter**: Automated delivery retries with exponential backoff and jitter calculations.
- **Dead-Letter Queue (DLQ)**: Exhausted delivery attempts are automatically isolated to a persistent DLQ for inspection and manual replay.
- **Pure Python**: Zero third-party dependencies required.

---

## 🏗️ Architecture

```
Incoming / Outgoing Webhook Event
              |
              v
     [HMAC Verifier]  ---> (Reject invalid signatures)
              |
     [Idempotency Check] ---> (Deduplicate repeated delivery)
              |
     [Delivery Pipeline]
              |
      +-------+-------+
      | (Success)     | (Failure / Timeout)
      v               v
  (200 OK)    [Exponential Backoff Retry Queue]
                      |
              +-------+-------+
              | (Retry < Max) | (Retry >= Max)
              v               v
          (Re-queue)      [Dead Letter Queue (DLQ)]
```

---

## 📦 Quickstart

### Installation

```bash
git clone https://github.com/Gaurav28-tech/relay-hub.git
cd relay-hub
```

### Basic Usage

```python
from relay.verifier import SignatureVerifier
from relay.queue import RetryQueue
from relay.models import WebhookEvent

# 1. Sign and Verify Webhooks
secret = "whsec_supersecretkey123"
payload = '{"event": "payment.succeeded", "amount": 4900}'
sig = SignatureVerifier.sign(payload, secret)

is_valid = SignatureVerifier.verify(payload, sig, secret)
print(f"Signature Valid: {is_valid}")

# 2. Queue with Exponential Backoff
queue = RetryQueue(max_retries=3, base_backoff_seconds=1.0)
event = WebhookEvent(
    id="evt_001",
    target_url="https://api.partner.com/webhook",
    payload=payload
)
queue.enqueue(event)
```

### Running Tests

```bash
python -m unittest discover -s tests -p "test_*.py"
```

---

## 📄 License

Distributed under the [MIT License](LICENSE).
