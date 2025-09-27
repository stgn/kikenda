from typing import Any, Protocol, cast


class Stage[A, B](Protocol):
    def forward(self, data: A) -> B: ...
    def inverse(self, data: B) -> A: ...


class _Identity[A](Stage[A, A]):
    def forward(self, data: A) -> A:
        return data

    def inverse(self, data: A) -> A:
        return data

    def __getitem__[B](self, ty: type[B]) -> "_Identity[B]":
        return cast("_Identity[B]", self)


Identity = _Identity[Any]()


class Parallel[LA, LB, RA, RB](Stage[tuple[LA, RA], tuple[LB, RB]]):
    __slots__ = "_left", "_right"

    def __init__(self, left: Stage[LA, LB], right: Stage[RA, RB]):
        self._left = left
        self._right = right

    def forward(self, data: tuple[LA, RA]) -> tuple[LB, RB]:
        ld, rd = data
        return self._left.forward(ld), self._right.forward(rd)

    def inverse(self, data: tuple[LB, RB]) -> tuple[LA, RA]:
        ld, rd = data
        return self._left.inverse(ld), self._right.inverse(rd)


class Composed[A, B, C](Stage[A, C]):
    __slots__ = "_prev", "_next"

    def __init__(self, prev: Stage[A, B], next_: Stage[B, C]):
        self._prev = prev
        self._next = next_

    def forward(self, data: A) -> C:
        return self._next.forward(self._prev.forward(data))

    def inverse(self, data: C) -> A:
        return self._prev.inverse(self._next.inverse(data))
