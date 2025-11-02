import sys
from collections.abc import Callable, Iterable, Sequence
from operator import itemgetter
from typing import overload

from misclib.protocols import SupportsRichComparison

__all__ = 'binary_search', 'max_with_index', 'min_with_index', 'sorted_with_indices'


def binary_search[T: SupportsRichComparison](
        seq: Sequence[T],
        value: T,
        start: int = 0,
        /,
        stop: int = sys.maxsize,
        ) -> int:
    """
    Searches for the given value in the given **sorted** sequence.
    If the value is present, then returns any index where this value is stored,
    or ``-1`` otherwise.

    Parameters `start` and `stop` specify a slice of this sequence
    where the search is done without creating an actual slice.

    >>> from misclib.functions.indexing import binary_search
    >>> li = [1, 2, 3, 4, 5]
    >>> binary_search(li, 4)
    3
    >>> binary_search(li, 0)
    -1
    >>> binary_search(li, 4, stop=3)
    -1
    >>> binary_search(li, 4, 3, 5)
    3
    >>> li = [1, 2, 3, 3, 4, 5]
    >>> binary_search(li, 3)
    3
    >>> li = [1, 2, 2, 3, 4, 5]
    >>> binary_search(li, 2)
    1
    """
    start, stop, _ = slice(start, stop).indices(len(seq))
    while start < stop:
        mid = start + (stop - start) // 2
        mid_value = seq[mid]
        if value is mid_value or value == mid_value:
            return mid

        if value < mid_value:
            stop = mid
        else:
            start = mid + 1

    return -1


type KeyFunc[T] = Callable[[T], SupportsRichComparison]
_last_in_pair = itemgetter(1)
_sentinel = object()


@overload
def max_with_index[T: SupportsRichComparison](
        value1: T,
        value2: T,
        /,
        *values: T,
        key: None = None,
        ) -> tuple[int, T]: ...


@overload
def max_with_index[T](
        value1: T,
        value2: T,
        /,
        *values: T,
        key: KeyFunc[T],
        ) -> tuple[int, T]: ...


@overload
def max_with_index[T: SupportsRichComparison](
        iterable: Iterable[T],
        /,
        *,
        key: None = None,
        ) -> tuple[int, T]: ...


@overload
def max_with_index[T](
        iterable: Iterable[T],
        /,
        *,
        key: KeyFunc[T],
        ) -> tuple[int, T]: ...


@overload
def max_with_index[T: SupportsRichComparison, D](
        iterable: Iterable[T],
        /,
        *,
        key: None = None,
        default: D,
        ) -> tuple[int, T] | D: ...


@overload
def max_with_index[T, D](
        iterable: Iterable[T],
        /,
        *,
        key: KeyFunc[T],
        default: D,
        ) -> tuple[int, T] | D: ...


def max_with_index[T, D](
        *values: T,
        key: KeyFunc[T] | None = None,
        default: D = _sentinel,
        ) -> T | D:
    """
    With a single :class:`Iterable` argument,
    returns its greatest item and the zero-based position of this item.
    The iterable cannot be empty unless `default` is provided;
    in such case returns the value of this parameter.

    >>> from misclib.functions.indexing import max_with_index
    >>> max_with_index('edcba')
    (0, 'e')
    >>> max_with_index('')
    Traceback (most recent call last):
        ...
    ValueError: max() iterable argument is empty
    >>> max_with_index('', default=-1)
    -1

    With two or more arguments,
    returns the greatest argument with its zero-based position.

    >>> max_with_index('c', 'a', 'e', 'd', 'b')
    (2, 'e')
    """
    if len(values) == 1:
        values = values[0]

    iterable = enumerate(values)
    compare = _last_in_pair if key is None else (lambda pair: key(pair[1]))
    if default is _sentinel:
        return max(iterable, key=compare)

    return max(iterable, key=compare, default=default)


@overload
def min_with_index[T: SupportsRichComparison](
        value1: T,
        value2: T,
        /,
        *values: T,
        key: None = None,
        ) -> tuple[int, T]: ...


@overload
def min_with_index[T](
        value1: T,
        value2: T,
        /,
        *values: T,
        key: KeyFunc[T],
        ) -> tuple[int, T]: ...


@overload
def min_with_index[T: SupportsRichComparison](
        iterable: Iterable[T],
        /,
        *,
        key: None = None,
        ) -> tuple[int, T]: ...


@overload
def min_with_index[T](
        iterable: Iterable[T],
        /,
        *,
        key: KeyFunc[T],
        ) -> tuple[int, T]: ...


@overload
def min_with_index[T: SupportsRichComparison, D](
        iterable: Iterable[T],
        /,
        *,
        key: None = None,
        default: D,
        ) -> tuple[int, T] | D: ...


@overload
def min_with_index[T, D](
        iterable: Iterable[T],
        /,
        *,
        key: KeyFunc[T],
        default: D,
        ) -> tuple[int, T] | D: ...


def min_with_index[T, D](
        *values: T,
        key: KeyFunc[T] | None = None,
        default: D = _sentinel,
        ) -> T | D:
    """
    With a single :class:`Iterable` argument,
    returns its least item and the zero-based position of this item.
    The iterable cannot be empty unless `default` is provided;
    in such case returns the value of this parameter.

    >>> from misclib.functions.indexing import min_with_index
    >>> min_with_index('edcba')
    (4, 'a')
    >>> min_with_index('')
    Traceback (most recent call last):
        ...
    ValueError: min() iterable argument is empty
    >>> min_with_index('', default=-1)
    -1

    With two or more arguments,
    returns the least argument with its zero-based position.

    >>> min_with_index('c', 'a', 'e', 'd', 'b')
    (1, 'a')
    """
    if len(values) == 1:
        values = values[0]

    iterable = enumerate(values)
    compare = _last_in_pair if key is None else (lambda pair: key(pair[1]))
    if default is _sentinel:
        return min(iterable, key=compare)

    return min(iterable, key=compare, default=default)


@overload
def sorted_with_indices[T: SupportsRichComparison](
        iterable: Iterable[T],
        /,
        *,
        key: None = None,
        reverse: bool = False,
        ) -> list[tuple[int, T]]: ...


@overload
def sorted_with_indices[T](
        iterable: Iterable[T],
        /,
        *,
        key: KeyFunc[T],
        reverse: bool = False,
        ) -> list[tuple[int, T]]: ...


def sorted_with_indices[T](
        iterable: Iterable[T],
        /,
        *,
        key: KeyFunc[T] | None = None,
        reverse: bool = False,
        ) -> list[tuple[int, T]]:
    # noinspection PyUnresolvedReferences
    """
    Returns a new list containing all items
    from the given iterable in ascending order
    coupled with their original indices.

    >>> from misclib.functions.indexing import sorted_with_indices
    >>> sorted_with_indices('edcba')
    [(4, 'a'), (3, 'b'), (2, 'c'), (1, 'd'), (0, 'e')]

    A custom key function can be supplied to customize the sort order,
    and the reverse flag can be set to request the result in descending order.

    >>> sorted_with_indices('edcba', reverse=True)
    [(0, 'e'), (1, 'd'), (2, 'c'), (3, 'b'), (4, 'a')]
    >>> sorted_with_indices('edcba', key=lambda x: 99 - ord(x))
    [(0, 'e'), (1, 'd'), (2, 'c'), (3, 'b'), (4, 'a')]

    To obtain two separate lists -
    one with original indices and one with sorted items -
    use the next code snippet:

    >>> iterable_ = 'edcba'  # your iterable
    >>> indices_items = sorted_with_indices(iterable_)
    >>> indices, items = (list(i_v) for i_v in zip(*indices_items))
    >>> indices
    [4, 3, 2, 1, 0]
    >>> items
    ['a', 'b', 'c', 'd', 'e']
    """
    return sorted(
        enumerate(iterable),
        key=_last_in_pair if key is None else (lambda pair: key(pair[1])),
        reverse=reverse,
        )
