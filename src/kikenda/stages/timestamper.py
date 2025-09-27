from datetime import datetime
from io import BytesIO

from ..pipeline import Stage
from ..varint import uleb128


class _Timestamper(Stage[tuple[bytes, datetime], bytes]):
    def forward(self, data: tuple[bytes, datetime]) -> bytes:
        payload, ts = data
        ts = int(ts.timestamp())
        return b"".join((uleb128.encode(ts), payload))

    def inverse(self, data: bytes) -> tuple[bytes, datetime]:
        bio = BytesIO(data)
        ts, _ = uleb128.decode_reader(bio)
        ts = datetime.fromtimestamp(ts)
        payload = bio.read()
        return payload, ts


Timestamper = _Timestamper()
