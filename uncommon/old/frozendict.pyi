from __future__ import annotations

from collections.abc import ItemsView, Iterable, Iterator, KeysView, Mapping, ValuesView
from typing import Any, Generic, TypeVar, Union, overload

_K = TypeVar('_K')
_V_co = TypeVar('_V_co', covariant=True)
_T = TypeVar('_T')


class frozendict(Generic[_K, _V_co]):
    @overload
    def __init__(self, **kwargs: _V_co): ...
    @overload
    def __init__(self, map: Mapping[_K, _V_co], /, **kwargs: _V_co): ...
    @overload
    def __init__(self, iterable: Iterable[tuple[_K, _V_co]], /, **kwargs: _V_co): ...
    def copy(self, /) -> frozendict: ...
    @classmethod
    @overload
    def fromkeys(cls, iterable: Iterable[_K], /) -> frozendict[_K, None]: ...
    @classmethod
    @overload
    def fromkeys(cls, iterable: Iterable[_K], value: _T, /) -> frozendict[_K, _T]: ...
    @overload
    def get(self, key: _K, /) -> _V_co: ...
    @overload
    def get(self, key: _K, default: Union[_V_co, _T], /) -> Union[_V_co, _T]: ...
    def items(self, /) -> ItemsView[_K, _V_co]: ...
    def keys(self, /) -> KeysView[_K]: ...
    def values(self, /) -> ValuesView[_V_co]: ...
    def __contains__(self, item: Any, /) -> bool: ...
    def __getitem__(self, k: _K, /) -> _V_co: ...
    def __hash__(self, /) -> int: ...
    def __iter__(self, /) -> Iterator[_K]: ...
    def __len__(self, /) -> int: ...
    def __reversed__(self, /) -> Iterator[_K]: ...
    def __or__(self, other: Mapping, /) -> frozendict: ...
    def __ror__(self, other: Mapping, /) -> Mapping: ...
