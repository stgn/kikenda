from io import BytesIO

from ..pipeline import Stage
from ..varint import uleb128


class _Joiner(Stage[tuple[bytes, bytes], bytes]):
    def forward(self, data: tuple[bytes, bytes]) -> bytes:
        left, right = data
        return b"".join((uleb128.encode(len(left)), left, right))

    def inverse(self, data: bytes) -> tuple[bytes, bytes]:
        bio = BytesIO(data)
        left_len, _ = uleb128.decode_reader(bio)
        left = bio.read(left_len)
        right = bio.read()
        return left, right


Joiner = _Joiner()
