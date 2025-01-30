from collections.abc import Callable, Iterable
from operator import itemgetter
from typing import overload

from misclib.protocols import SupportsRichComparison


# todo
#  add binary_search
#  add safe tuple comparisons

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
    The iterable cannot be empty unless parameter ``default`` is provided;
    in such case returns the value of this parameter.

    With two or more arguments,
    returns the greatest argument with its zero-based position.
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
    The iterable cannot be empty unless parameter ``default`` is provided;
    in such case returns the value of this parameter.

    With two or more arguments,
    returns the least argument with its zero-based position.
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

        A custom key function can be supplied to customize the sort order,
        and the reverse flag can be set to request the result in descending order.

        To obtain two separate lists -
        one with original indices and one with sorted items -
        use the next code snippet:

        >>> iterable_ = 'parent'  # your iterable
        >>> indices_items = sorted_with_indices(iterable_)
        >>> indices, items = (list(tuple_) for tuple_ in zip(*items_indices))
        """
    return sorted(
        enumerate(iterable),
        key=_last_in_pair if key is None else (lambda pair: key(pair[1])),
        reverse=reverse,
        )


__all__ = 'max_with_index', 'min_with_index', 'sorted_with_indices'
