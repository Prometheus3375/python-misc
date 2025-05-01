from types import TracebackType
from typing import Self


class Supress:
    """
    A context manager for suppressing specific exception types.

    >>> from misclib.context import Supress
    >>> 1 / 0
    Traceback (most recent call last):
        ...
    ZeroDivisionError: division by zero
    >>> with Supress(ZeroDivisionError):
    ...     1 / 0
    ...

    The supression is also applied for subclasses of the specified exception type:

    >>> issubclass(ZeroDivisionError, ArithmeticError)
    True
    >>> with Supress(ArithmeticError):
    ...     1 / 0
    ...

    The manager does not supress errors that are not a subtype of the specified one:

    >>> with Supress(ValueError):
    ...     1 / 0
    ...
    Traceback (most recent call last):
        ...
    ZeroDivisionError: division by zero

    To supress several exceptions types, pass them to the constructor:

    >>> with Supress(ZeroDivisionError, ValueError):
    ...     1 / 0
    ...
    """
    __slots__ = '_error_classes',

    def __init__(self, exc_type: type[BaseException], /, *exc_types: type[BaseException]) -> None:
        exception_types = exc_type, *exc_types
        for i, exc_type in enumerate(exception_types):
            if not (isinstance(exc_type, type) and issubclass(exc_type, BaseException)):
                raise TypeError(
                    f'expected a subclass of {BaseException.__name__}, '
                    f'got {exc_type!r} at position {i}'
                    )

        self._error_classes = exception_types

    def __enter__(self, /) -> Self:
        return self

    def __exit__(
            self,
            exc_type: type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None,
            /,
            ) -> bool:
        return exc_type and issubclass(exc_type, self._error_classes)


__all__ = 'Supress',
