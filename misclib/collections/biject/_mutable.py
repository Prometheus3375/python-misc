from collections.abc import Iterable, Mapping
from typing import Union, overload

from ._abstract import AbstractBijectiveMap, P, T, T1, T2, V, dummy, unique_pairs


class BijectiveMap(AbstractBijectiveMap):
    def set(self, v1: T1, v2: T2, /):
        self._data.pop(self._data.pop(v1, dummy), dummy)
        self._data.pop(self._data.pop(v2, dummy), dummy)
        self._data[v1] = v2
        self._data[v2] = v1

    def add(self, v1: T1, v2: T2, /):
        if v1 in self._data:
            v = v1
        elif v2 in self._data:
            v = v2
        else:
            self._data[v1] = v2
            self._data[v2] = v1
            return

        raise ValueError(f'value {v} is already bound to {self[v]}')

    @overload
    def update(self, other: Mapping[T1, T2], /): ...
    @overload
    def update(self, other: Mapping[str, T2], /, **kwargs: T2): ...
    @overload
    def update(self, other: Mapping[T1, str], /, **kwargs: T1): ...
    @overload
    def update(self, other: Iterable[P], /): ...
    @overload
    def update(self, other: Iterable[tuple[str, T2]], /, **kwargs: T2): ...
    @overload
    def update(self, other: Iterable[tuple[T1, str]], /, **kwargs: T1): ...

    def update(self, other=(), /, **kwargs):
        unique_pairs(other, kwargs, mapping=self._data)

    @overload
    def pop(self, value: T1, /) -> T2: ...
    @overload
    def pop(self, value: T2, /) -> T1: ...
    @overload
    def pop(self, value: T1, default: T2, /) -> T2: ...
    @overload
    def pop(self, value: T1, default: T, /) -> Union[T2, T]: ...
    @overload
    def pop(self, value: T2, default: T1, /) -> T1: ...
    @overload
    def pop(self, value: T2, default: T, /) -> Union[T1, T]: ...

    def pop(self, value, default=dummy, /):
        if default is not dummy and value not in self._data:
            return default

        v = self._data.pop(value)
        self._data.__delitem__(v)
        return v

    def popitem(self, /) -> P:
        self._data.popitem()  # pops (v2, v1)
        return self._data.popitem()

    def __delitem__(self, value: V, /):
        self._data.__delitem__(self._data.pop(value))

    def clear(self, /):
        self._data.clear()
