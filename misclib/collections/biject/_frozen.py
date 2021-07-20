from collections.abc import Iterable, Mapping
from sys import getsizeof
from typing import overload

from ._abstract import AbstractBijectiveMap, P_co, T1_co, T2_co


class FrozenBijectiveMap(AbstractBijectiveMap[T1_co, T2_co]):
    __slots__ = '_hash',

    @overload
    def __init__(self, mapping: Mapping[T1_co, T2_co], /): ...
    @overload
    def __init__(self, iterable: Iterable[P_co], /): ...
    @overload
    def __init__(self, /): ...

    def __init__(self, data=(), /):
        super().__init__(data)
        self._hash = hash(frozenset(frozenset(pair) for pair in self.pairs()))

    def __hash__(self, /):
        return self._hash

    def __sizeof__(self, /):
        return super().__sizeof__() + getsizeof(self._hash)
