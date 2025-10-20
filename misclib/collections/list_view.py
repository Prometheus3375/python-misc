import sys
from collections.abc import Iterator, Sequence
from typing import Any, overload

type ListOrView[T] = list[T] | ListView[T]


@Sequence.register
class ListView[T]:
    """
    A view for protecting lists from mutations.
    Behaves as a proxy object.
    """
    __slots__ = '_source',

    def __init__(self, source: ListOrView[T], /) -> None:
        if isinstance(source, list):
            self._source = source
        elif isinstance(source, ListView):
            self._source = source._source
        else:
            raise TypeError(
                f'source must be a list or a {self.__class__.__name__}, '
                f'got {type(source)}'
                )

    def __len__(self, /) -> int:
        return len(self._source)

    def __iter__(self, /) -> Iterator[T]:
        return iter(self._source)

    def __reversed__(self, /) -> Iterator[T]:
        return reversed(self._source)

    def __contains__(self, item: Any, /) -> bool:
        return item in self._source

    @overload
    def __getitem__(self, item: int, /) -> T: ...
    @overload
    def __getitem__(self, item: slice, /) -> list[T]: ...

    def __getitem__(self, item: int | slice, /) -> T | list[T]:
        return self._source[item]

    def __repr__(self, /) -> str:
        return f'{self.__class__.__name__}({self._source})'

    def copy(self, /) -> list[T]:
        """
        Returns a shallow copy of the wrapped list.
        """
        return self._source.copy()

    def index(self, value: T, start: int = 0, stop: int = sys.maxsize, /) -> int:
        """
        If a value is present in the wrapped list,
        returns an index of its first occurrence,
        and raises :class:`ValueError` otherwise.
        """
        return self._source.index(value, start, stop)

    def count(self, value: T, /) -> int:
        """
        Returns the number of occurrences of a value in the wrapped list.
        """
        return self._source.count(value)

    def __mul__(self, other: int, /) -> list[T]:
        return self._source * other

    __rmul__ = __mul__

    def __add__(self, other: ListOrView, /) -> list[T]:
        return self._source + other

    def __radd__(self, other: ListOrView, /) -> list[T]:
        return other + self._source

    def __eq__(self, other: Any, /) -> bool:
        return other == self._source

    def __ne__(self, other: Any, /) -> bool:
        return other != self._source

    def __gt__(self, other: ListOrView, /) -> bool:
        return self._source > other

    def __ge__(self, other: ListOrView, /) -> bool:
        return self._source >= other

    def __lt__(self, other: ListOrView, /) -> bool:
        return self._source < other

    def __le__(self, other: ListOrView, /) -> bool:
        return self._source <= other


__all__ = 'ListView', 'ListOrView'
