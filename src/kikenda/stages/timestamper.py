from io import BytesIO
from time import time

from ..exc import BadTimestamp
from ..pipeline import Stage
from ..varint import uleb128


class Timestamper(Stage[bytes, bytes]):
    def __init__(self, max_age: int):
        self._max_age = max_age

    def forward(self, data: bytes) -> bytes:
        ts = int(time())
        return b"".join((uleb128.encode(ts), data))

    def inverse(self, data: bytes) -> bytes:
        bio = BytesIO(data)
        ts, _ = uleb128.decode_reader(bio)
        age = time() - ts
        if age > self._max_age:
            raise BadTimestamp
        return bio.read()
