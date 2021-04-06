from collections.abc import Iterable
from typing import Protocol, TypeVar

K = TypeVar('K')
T = TypeVar('T')
V_co = TypeVar('V_co', covariant=True)


class SupportsKeysAndGetItem(Protocol[K, V_co]):
    def keys(self, /) -> Iterable[K]: ...
    def __getitem__(self, item: K, /) -> V_co: ...


class SupportsLessThan(Protocol[T]):
    def __lt__(self: T, other: T, /) -> bool: ...
