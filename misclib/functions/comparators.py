from collections.abc import Callable, Collection, Sequence
from typing import Any, NamedTuple

__all__ = (
    'ComparatorTuple',
    'create_sequence_comparators',
    'sequence_comparators',
    'sequence_safe_comparators',
    'tuple_safe_comparators',
    'sequence_eq',
    'sequence_ne',
    'sequence_lt',
    'sequence_le',
    'sequence_gt',
    'sequence_ge',
    'sequence_safe_lt',
    'sequence_safe_le',
    'sequence_safe_gt',
    'sequence_safe_ge',
    'tuple_safe_lt',
    'tuple_safe_le',
    'tuple_safe_gt',
    'tuple_safe_ge',
    'define_safe_tuple_comparators',
    )


class ComparatorTuple[T](NamedTuple):
    """
    A holder of comparison functions.

    These functions can return ``NotImplemented``
    if their operation is not supported for the object passed as the second argument.
    """
    eq: Callable[[T, Any], bool]
    ne: Callable[[T, Any], bool]
    lt: Callable[[T, T], bool]
    le: Callable[[T, T], bool]
    gt: Callable[[T, T], bool]
    ge: Callable[[T, T], bool]


def create_sequence_comparators[T: Collection](
        upper_class: type[T],
        /,
        *,
        safe_inequalities: bool,
        ) -> ComparatorTuple[T]:
    """
    Creates comparison functions for sequences.

    It is assumed that the first argument of these functions
    is always an instance of `upper_class` or of its subclass.
    If the second argument is not an instance of `upper_class`,
    the functions return ``NotImplemented``.

    If `safe_inequalities` is ``True``,
    then functions ``lt``, ``le``, ``gt`` and ``ge`` specially handle ``None``
    considering it as the lowest value.
    """
    def __eq__(self: T, other: Any, /) -> bool:
        f"""
        Determines whether the given instance of :class:`{upper_class.__name__}`
        is equal to the other given object.
        """
        if isinstance(other, upper_class):
            return (
                    len(self) == len(other)
                    and all(v1 is v2 or v1 == v2 for v1, v2 in zip(self, other))
            )

        return NotImplemented

    def __ne__(self: T, other: Any, /) -> bool:
        f"""
        Determines whether the given instance of :class:`{upper_class.__name__}`
        is NOT equal to the other given object.
        """
        if isinstance(other, upper_class):
            return (
                    len(self) != len(other)
                    or any(v1 is not v2 and v1 != v2 for v1, v2 in zip(self, other))
            )

        return NotImplemented

    if safe_inequalities:
        def __lt__(self: T, other: T, /) -> bool:
            f"""
            Determines whether the given instance of :class:`{upper_class.__name__}`
            is strictly lower than the other one.
            """
            if isinstance(other, upper_class):
                for v1, v2 in zip(self, other):
                    if v1 is not v2 and v1 != v2:
                        if v1 is None: return True
                        if v2 is None: return False
                        return v1 < v2

                # At this point all values up to the lower length are equal.
                return len(self) < len(other)

            return NotImplemented

        def __le__(self: T, other: T, /) -> bool:
            f"""
            Determines whether the given instance of :class:`{upper_class.__name__}`
            is equal to or lower than the other one.
            """
            if isinstance(other, upper_class):
                for v1, v2 in zip(self, other):
                    if v1 is not v2 and v1 != v2:
                        if v1 is None: return True
                        if v2 is None: return False
                        return v1 < v2

                # At this point all values up to the lower length are equal.
                return len(self) <= len(other)

            return NotImplemented

        def __gt__(self: T, other: T, /) -> bool:
            f"""
            Determines whether the given instance of :class:`{upper_class.__name__}`
            is strictly greater than the other one.
            """
            if isinstance(other, upper_class):
                for v1, v2 in zip(self, other):
                    if v1 is not v2 and v1 != v2:
                        if v1 is None: return False
                        if v2 is None: return True
                        return v1 > v2

                # At this point all values up to the lower length are equal.
                return len(self) > len(other)

            return NotImplemented

        def __ge__(self: T, other: T, /) -> bool:
            f"""
            Determines whether the given instance of :class:`{upper_class.__name__}`
            is equal to or greater than the other one.
            """
            if isinstance(other, upper_class):
                for v1, v2 in zip(self, other):
                    if v1 is not v2 and v1 != v2:
                        if v1 is None: return False
                        if v2 is None: return True
                        return v1 > v2

                # At this point all values up to the lower length are equal.
                return len(self) >= len(other)

            return NotImplemented

    else:
        def __lt__(self: T, other: T, /) -> bool:
            f"""
            Determines whether the given instance of :class:`{upper_class.__name__}`
            is strictly lower than the other one.
            """
            if isinstance(other, upper_class):
                for v1, v2 in zip(self, other):
                    if v1 is not v2 and v1 != v2:
                        return v1 < v2

                # At this point all values up to the lower length are equal.
                return len(self) < len(other)

            return NotImplemented

        def __le__(self: T, other: T, /) -> bool:
            f"""
            Determines whether the given instance of :class:`{upper_class.__name__}`
            is equal to or lower than the other one.
            """
            if isinstance(other, upper_class):
                for v1, v2 in zip(self, other):
                    if v1 is not v2 and v1 != v2:
                        return v1 < v2

                # At this point all values up to the lower length are equal.
                return len(self) <= len(other)

            return NotImplemented

        def __gt__(self: T, other: T, /) -> bool:
            f"""
            Determines whether the given instance of :class:`{upper_class.__name__}`
            is strictly greater than the other one.
            """
            if isinstance(other, upper_class):
                for v1, v2 in zip(self, other):
                    if v1 is not v2 and v1 != v2:
                        return v1 > v2

                # At this point all values up to the lower length are equal.
                return len(self) > len(other)

            return NotImplemented

        def __ge__(self: T, other: T, /) -> bool:
            f"""
            Determines whether the given instance of :class:`{upper_class.__name__}`
            is equal to or greater than the other one.
            """
            if isinstance(other, upper_class):
                for v1, v2 in zip(self, other):
                    if v1 is not v2 and v1 != v2:
                        return v1 > v2

                # At this point all values up to the lower length are equal.
                return len(self) >= len(other)

            return NotImplemented

    return ComparatorTuple(eq=__eq__, ne=__ne__, lt=__lt__, le=__le__, gt=__gt__, ge=__ge__)


sequence_comparators = create_sequence_comparators(Sequence, safe_inequalities=False)
"""
An object containing references to comparators for sequences.
Unlike defined functions in this module, referenced function can return ``
"""
sequence_safe_comparators = create_sequence_comparators(Sequence, safe_inequalities=True)
tuple_safe_comparators = create_sequence_comparators(tuple, safe_inequalities=True)
# Remove redundancy in functions.
sequence_safe_comparators = ComparatorTuple(
    eq=sequence_comparators.eq,
    ne=sequence_comparators.ne,
    lt=sequence_safe_comparators.lt,
    le=sequence_safe_comparators.le,
    gt=sequence_safe_comparators.gt,
    ge=sequence_safe_comparators.ge,
    )
tuple_safe_comparators = ComparatorTuple(
    eq=tuple.__eq__,
    ne=tuple.__ne__,
    lt=tuple_safe_comparators.lt,
    le=tuple_safe_comparators.le,
    gt=tuple_safe_comparators.gt,
    ge=tuple_safe_comparators.ge,
    )


def sequence_eq(seq: Sequence, other: Any, /) -> bool:
    """
    Determines whether the given instance of :class:`Sequence`
    is equal to the other given object.

    This function always returns a boolean value.
    """
    return False if (result := sequence_comparators.eq(seq, other)) is NotImplemented else result


def sequence_ne(seq: Sequence, other: Any, /) -> bool:
    """
    Determines whether the given instance of :class:`Sequence`
    is NOT equal to the other given object.

    This function always returns a boolean value.
    """
    return False if (result := sequence_comparators.ne(seq, other)) is NotImplemented else result


def sequence_lt(seq: Sequence, other: Sequence, /) -> bool:
    """
    Determines whether the given instance of :class:`Sequence`
    is strictly lower than the other one.

    This function always returns a boolean value.
    """
    return False if (result := sequence_comparators.lt(seq, other)) is NotImplemented else result


def sequence_le(seq: Sequence, other: Sequence, /) -> bool:
    """
    Determines whether the given instance of :class:`Sequence`
    is equal to or lower than the other one.

    This function always returns a boolean value.
    """
    return False if (result := sequence_comparators.le(seq, other)) is NotImplemented else result


def sequence_gt(seq: Sequence, other: Sequence, /) -> bool:
    """
    Determines whether the given instance of :class:`Sequence`
    is strictly greater than the other one.

    This function always returns a boolean value.
    """
    return False if (result := sequence_comparators.gt(seq, other)) is NotImplemented else result


def sequence_ge(seq: Sequence, other: Sequence, /) -> bool:
    """
    Determines whether the given instance of :class:`Sequence`
    is equal to or greater than the other one.

    This function always returns a boolean value.
    """
    return False if (result := sequence_comparators.ge(seq, other)) is NotImplemented else result


def sequence_safe_lt(seq: Sequence, other: Sequence, /) -> bool:
    """
    Determines whether the given instance of :class:`Sequence`
    is strictly lower than the other one.

    Element-to-element comparisons do not raise :class:`TypeError` if one of them is ``None``.

    This function always returns a boolean value.
    """
    return (
        False
        if (result := sequence_safe_comparators.lt(seq, other)) is NotImplemented
        else result
    )


def sequence_safe_le(seq: Sequence, other: Sequence, /) -> bool:
    """
    Determines whether the given instance of :class:`Sequence`
    is equal to or lower than the other one.

    Element-to-element comparisons do not raise :class:`TypeError` if one of them is ``None``.

    This function always returns a boolean value.
    """
    return (
        False
        if (result := sequence_safe_comparators.le(seq, other)) is NotImplemented
        else result
    )


def sequence_safe_gt(seq: Sequence, other: Sequence, /) -> bool:
    """
    Determines whether the given instance of :class:`Sequence`
    is strictly greater than the other one.

    Element-to-element comparisons do not raise :class:`TypeError` if one of them is ``None``.

    This function always returns a boolean value.
    """
    return (
        False
        if (result := sequence_safe_comparators.gt(seq, other)) is NotImplemented
        else result
    )


def sequence_safe_ge(seq: Sequence, other: Sequence, /) -> bool:
    """
    Determines whether the given instance of :class:`Sequence`
    is equal to or greater than the other one.

    Element-to-element comparisons do not raise :class:`TypeError` if one of them is ``None``.

    This function always returns a boolean value.
    """
    return (
        False
        if (result := sequence_safe_comparators.ge(seq, other)) is NotImplemented
        else result
    )


def tuple_safe_lt(seq: tuple, other: tuple, /) -> bool:
    """
    Determines whether the given instance of :class:`tuple`
    is strictly lower than the other one.

    Element-to-element comparisons do not raise :class:`TypeError` if one of them is ``None``.

    This function always returns a boolean value.
    """
    return (
        False
        if (result := tuple_safe_comparators.lt(seq, other)) is NotImplemented
        else result
    )


def tuple_safe_le(seq: tuple, other: tuple, /) -> bool:
    """
    Determines whether the given instance of :class:`tuple`
    is equal to or lower than the other one.

    Element-to-element comparisons do not raise :class:`TypeError` if one of them is ``None``.

    This function always returns a boolean value.
    """
    return (
        False
        if (result := tuple_safe_comparators.le(seq, other)) is NotImplemented
        else result
    )


def tuple_safe_gt(seq: tuple, other: tuple, /) -> bool:
    """
    Determines whether the given instance of :class:`tuple`
    is strictly greater than the other one.

    Element-to-element comparisons do not raise :class:`TypeError` if one of them is ``None``.

    This function always returns a boolean value.
    """
    return (
        False
        if (result := tuple_safe_comparators.gt(seq, other)) is NotImplemented
        else result
    )


def tuple_safe_ge(seq: tuple, other: tuple, /) -> bool:
    """
    Determines whether the given instance of :class:`tuple`
    is equal to or greater than the other one.

    Element-to-element comparisons do not raise :class:`TypeError` if one of them is ``None``.

    This function always returns a boolean value.
    """
    return (
        False
        if (result := tuple_safe_comparators.ge(seq, other)) is NotImplemented
        else result
    )


def define_safe_tuple_comparators[T: tuple](cls: type[T], /) -> type[T]:
    """
    A decorator for tuple subclasses
    that replaces inherited comparison operators with such ones
    that handle element-to-element comparisons when one of them is ``None``.

    Any non-``None`` value is greater than ``None``.
    """
    # When using max, gt is used if available.
    # When using min, lt is used if available.
    # When using sorted, gt or lt are used based of reverse flag.
    # To avoid different behaviour, all comparators must be updated, not just lt.
    cls.__lt__ = tuple_safe_comparators.lt
    cls.__le__ = tuple_safe_comparators.le
    cls.__gt__ = tuple_safe_comparators.gt
    cls.__ge__ = tuple_safe_comparators.ge
    return cls
