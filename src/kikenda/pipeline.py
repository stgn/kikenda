from typing import Protocol, overload


class Stage[A, B](Protocol):
    def forward(self, data: A) -> B: ...
    def inverse(self, data: B) -> A: ...


class _EmptyPipeline:
    def then[A, B](self, next_: Stage[A, B]) -> "Pipeline[A, B]":
        return Pipeline(next_)

    def __or__[A, B](self, next_: Stage[A, B]) -> "Pipeline[A, B]":
        return self.then(next_)


EmptyPipeline = _EmptyPipeline()


class Composed[A, B, C](Stage[A, C]):
    __slots__ = "prev", "next"

    def __init__(self, prev: Stage[A, B], next_: Stage[B, C]):
        self.prev = prev
        self.next = next_

    def forward(self, data: A) -> C:
        return self.next.forward(self.prev.forward(data))

    def inverse(self, data: C) -> A:
        return self.prev.inverse(self.next.inverse(data))


class Pipeline[A, B](Stage[A, B]):
    __slots__ = ("_stage",)

    @overload
    def __new__(cls) -> _EmptyPipeline: ...

    @overload
    def __new__(cls, stage: Stage[A, B]) -> "Pipeline[A, B]": ...

    def __new__(
        cls, stage: Stage[A, B] | None = None
    ) -> "Pipeline[A, B] | _EmptyPipeline":
        if stage is None:
            return EmptyPipeline
        return super().__new__(cls)

    def __init__(self, stage: Stage[A, B] | None = None):
        assert stage is not None
        self._stage = stage

    def forward(self, data: A) -> B:
        return self._stage.forward(data)

    def inverse(self, data: B) -> A:
        return self._stage.inverse(data)

    def then[C](self, next_: Stage[B, C]) -> "Pipeline[A, C]":
        return Pipeline(Composed(self._stage, next_))

    def __or__[C](self, next_: Stage[B, C]) -> "Pipeline[A, C]":
        return self.then(next_)
