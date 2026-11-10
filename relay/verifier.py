import hmac
import hashlib

class SignatureVerifier:
    @staticmethod
    def sign(payload: str, secret: str) -> str:
        digest = hmac.new(
            secret.encode("utf-8"),
            payload.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
        return f"sha256={digest}"

    @staticmethod
    def verify(payload: str, signature_header: str, secret: str) -> bool:
        if not signature_header or not signature_header.startswith("sha256="):
            return False
        expected = SignatureVerifier.sign(payload, secret)
        return hmac.compare_digest(signature_header, expected)
