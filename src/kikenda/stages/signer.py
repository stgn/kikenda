import hashlib
from hmac import compare_digest
from typing import NamedTuple

from ..exc import BadSignature
from ..pipeline import Stage


class Envelope(NamedTuple):
    message: bytes
    signature: bytes


class Signer(Stage[bytes, tuple[bytes, bytes]]):
    def __init__(self, key: bytes, salt: bytes = b"kikenda", digest_size: int = 16):
        self._hasher = hashlib.blake2b(key=key, salt=salt, digest_size=digest_size)

    def _mac(self, data: bytes) -> bytes:
        hasher = self._hasher.copy()
        hasher.update(data)
        return hasher.digest()

    def forward(self, data: bytes) -> tuple[bytes, bytes]:
        return Envelope(data, self._mac(data))

    def inverse(self, data: tuple[bytes, bytes]) -> bytes:
        data = Envelope._make(data)
        mac = self._mac(data.message)
        if not compare_digest(mac, data.signature):
            raise BadSignature
        return data.message
