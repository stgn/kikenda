import base64

from ..exc import BadData
from ..pipeline import Stage

_invalid_trailing = [
    frozenset("BCDFGHJKLNOPRSTVWXZabdefhijlmnpqrtuvxyz1235679-_"),
    frozenset("EIMUYckos048"),
]


class _Base64(Stage[bytes, str]):
    def forward(self, data: bytes) -> str:
        return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")

    def inverse(self, data: str) -> bytes:
        pad_count = -len(data) % 4
        for i in range(pad_count):
            if data[-1] in _invalid_trailing[i]:
                raise BadData("non-canonical Base64 encoding detected")
        data += "=" * pad_count
        return base64.urlsafe_b64decode(data)


Base64 = _Base64()
