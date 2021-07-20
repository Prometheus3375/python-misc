from collections.abc import Iterable, Iterator, Mapping, MappingView, Set
from sys import getsizeof
from typing import Generic, Optional, TypeVar, Union, overload

T1 = TypeVar('T1')
T2 = TypeVar('T2')
V = Union[T1, T2]
P = tuple[T1, T2]

T1_co = TypeVar('T1_co', covariant=True)
T2_co = TypeVar('T2_co', covariant=True)
V_co = Union[T1_co, T2_co]
P_co = tuple[T1_co, T2_co]

T = TypeVar('T')

dummy = object()


@MappingView.register
class PairsView(Generic[T1, T2], Set[P]):
    __slots__ = '_source',

    def __init__(self, source: 'AbstractBijectiveMap[T1, T2]', /):
        self._source = source

    def __len__(self, /):
        return len(self._source) // 2

    def __contains__(self, pair: P, /):
        o = pair[0]
        os = self._source.get(pair[1], dummy)
        return o is os or o == os

    def __iter__(self, /) -> Iterator[P]:
        items = iter(self._source.items())
        for pair, _ in zip(items, items):
            yield pair

    def __reversed__(self, /) -> Iterator[P]:
        items = reversed(self._source.items())
        for _, pair in zip(items, items):
            yield pair

    def __repr__(self, /):
        return f'{self.__class__.__name__}({self._source!r})'

    @classmethod
    def _from_iterable(cls, iterable: Iterable[P], /):
        return set(iterable)


def unique_pairs(*data: Union[Mapping[T1, T2], Iterable[P]], mapping: dict[V, V] = None) -> dict[V, V]:
    d = {} if mapping is None else mapping
    for iterable in data:
        if isinstance(iterable, AbstractBijectiveMap):
            iterable = iterable.pairs()
        elif isinstance(iterable, Mapping):
            iterable = iterable.items()

        for value1, value2 in iterable:
            d.pop(d.pop(value1, dummy), dummy)
            d.pop(d.pop(value2, dummy), dummy)
            d[value1] = value2
            d[value2] = value1

    return d


@Mapping.register
class AbstractBijectiveMap(Generic[T1, T2]):
    __slots__ = '_data',

    @overload
    def __init__(self, mapping: Mapping[T1, T2], /): ...
    @overload
    def __init__(self, iterable: Iterable[P], /): ...
    @overload
    def __init__(self, /): ...

    def __init__(self, data=(), /):
        self._data: dict[V, V] = unique_pairs(data)

    def __len__(self, /):
        return len(self._data)

    @overload
    def __getitem__(self, value: T1, /) -> T2: ...
    @overload
    def __getitem__(self, value: T2, /) -> T1: ...

    def __getitem__(self, value, /):
        return self._data[value]

    def __contains__(self, value: V, /):
        return value in self._data

    def __iter__(self, /):
        return iter(self._data)

    def __reversed__(self, /):
        return reversed(self._data)

    @overload
    def get(self, value: T1, /) -> Optional[T2]: ...
    @overload
    def get(self, value: T2, /) -> Optional[T1]: ...
    @overload
    def get(self, value: T1, default: T2, /) -> T2: ...
    @overload
    def get(self, value: T1, default: T, /) -> Union[T2, T]: ...
    @overload
    def get(self, value: T2, default: T1, /) -> T1: ...
    @overload
    def get(self, value: T2, default: T, /) -> Union[T1, T]: ...

    def get(self, value, default=None, /):
        return self._data.get(value, default)

    def values(self, /):
        return self._data.keys()

    keys = values

    def items(self, /):
        return self._data.items()

    def pairs(self, /) -> PairsView[T1, T2]:
        return PairsView(self)

    def __str__(self, /):
        content = ', '.join(f'{v1} ~ {v2}' for v1, v2 in self.pairs())
        return f'{{{content}}}'

    def __repr__(self, /):
        return f'{self.__class__.__name__}({self})'

    def __eq__(self, other, /):
        return self._data == other

    def __ne__(self, other, /):
        return self._data != other

    def __getnewargs__(self, /) -> tuple[P, ...]:
        return tuple(self.pairs())

    def __sizeof__(self, /):
        return super().__sizeof__() + getsizeof(self._data)


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
    def update(self, other: Iterable[P], /): ...

    def update(self, other=(), /):
        unique_pairs(other, mapping=self._data)

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


__all__ = 'PairsView', 'AbstractBijectiveMap', 'BijectiveMap', 'FrozenBijectiveMap'
