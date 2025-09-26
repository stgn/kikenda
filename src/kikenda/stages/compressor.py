from typing import Protocol

from ..pipeline import Stage


class DataCompressor(Protocol):
    def compress(self, data: bytes, /) -> bytes: ...
    def decompress(self, data: bytes, /) -> bytes: ...


class Compressor(Stage[bytes, bytes]):
    def __init__(self, compressor: DataCompressor):
        self._compressor = compressor

    def forward(self, data: bytes) -> bytes:
        compressed = self._compressor.compress(data)
        if len(compressed) >= len(data):
            return b"\0" + data
        return b"\1" + compressed

    def inverse(self, data: bytes) -> bytes:
        is_compressed, data = data[0], data[1:]
        if is_compressed:
            return self._compressor.decompress(data)
        return data
