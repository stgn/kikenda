from typing import Any, Protocol

from ..pipeline import Stage


class DataSerializer(Protocol):
    def loads(self, data: bytes, /) -> Any: ...
    def dumps(self, obj: Any, /) -> bytes | str: ...


class Serializer(Stage[Any, bytes]):
    def __init__(self, serializer: DataSerializer):
        self._serializer = serializer

    def forward(self, data: Any) -> bytes:
        serialized = self._serializer.dumps(data)
        if isinstance(serialized, str):
            serialized = serialized.encode()
        return serialized

    def inverse(self, data: bytes) -> Any:
        return self._serializer.loads(data)
