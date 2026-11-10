<p align="center">
  <img src="assets/banner.svg" alt="Hookwire Banner" width="100%">
</p>

<p align="center">
  <a href="https://github.com/Gaurav28-tech/hookwire/actions"><img src="https://github.com/Gaurav28-tech/hookwire/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License"></a>
  <img src="https://img.shields.io/badge/Python-3.9+-brightgreen.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Delivery-Guaranteed%20Retry-emerald" alt="Delivery">
</p>

<p align="center">
  <b>Hookwire</b> is a resilient webhook delivery and ingestion pipeline built for event-driven microservices. It safeguards webhooks against replay attacks using cryptographic HMAC signatures, enforces idempotent execution, and guarantees at-least-once delivery with exponential backoff and Dead-Letter Queue (DLQ) support.
</p>

---

## ⚡ Live Terminal Preview

<p align="center">
  <img src="assets/demo.gif" alt="Hookwire Terminal Demo" width="100%">
</p>

---

## 🚀 Key Capabilities

- **HMAC-SHA256 Signatures**: Generates and verifies cryptographic signatures with constant-time comparison to prevent timing attacks.
- **Idempotency Guard**: Sliding TTL memory store ensuring incoming duplicate webhook deliveries are safely rejected.
- **Exponential Backoff**: Automated delivery retries with exponential backoff and jitter calculations.
- **Dead-Letter Queue (DLQ)**: Exhausted delivery attempts are automatically isolated to a persistent DLQ for inspection.
- **Zero Heavy Dependencies**: Pure standard library Python with zero broker dependencies.

---

## 🏗️ Architecture

<p align="center">
  <img src="assets/architecture.svg" alt="Hookwire Architecture" width="100%">
</p>

---

## 📦 Quickstart

### Installation

```bash
git clone https://github.com/Gaurav28-tech/hookwire.git
cd hookwire
```

### Basic Usage

```python
from relay.verifier import SignatureVerifier
from relay.queue import RetryQueue
from relay.models import WebhookEvent

# Sign and verify incoming webhook payloads
secret = "whsec_supersecretkey123"
payload = '{"event": "payment.succeeded", "amount": 4900}'
sig = SignatureVerifier.sign(payload, secret)

is_valid = SignatureVerifier.verify(payload, sig, secret)
print(f"Signature Valid: {is_valid}")

# Queue for resilient delivery with exponential backoff
queue = RetryQueue(max_retries=3, base_backoff_seconds=1.0)
event = WebhookEvent(id="evt_001", target_url="https://api.partner.com/webhook", payload=payload)
queue.enqueue(event)
```

### Running Test Suite

```bash
python -m unittest discover -s tests -p "test_*.py"
```

---

## 📄 License

Distributed under the [MIT License](LICENSE).
