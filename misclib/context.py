from types import TracebackType
from typing import Self


class Supress:
    """
    A context manager for suppressing specific exception types.

    >>> from misclib.context import Supress
    >>> result = 1
    >>> result
    1
    >>> with Supress(ZeroDivisionError):
    ...     error = 1 / 0
    ...     result = 10
    ...
    >>> result
    1
    >>> with Supress(ValueError):
    ...     error = 1 / 0
    ...     result = 10
    ...
    Traceback (most recent call last):
        ...
    ZeroDivisionError: division by zero

    The supression is also applied for subclasses of the specified exception type:

    >>> issubclass(ZeroDivisionError, ArithmeticError)
    True
    >>> with Supress(ArithmeticError):
    ...     error = 1 / 0
    ...     result = 10
    ...
    >>> result
    1
    """
    __slots__ = '_exc_cls',

    def __init__(self, exception_type: type[BaseException], /) -> None:
        self._exc_cls = exception_type

    def __enter__(self, /) -> Self:
        return self

    def __exit__(
            self,
            exc_type: type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None,
            /,
            ) -> bool:
        return exc_type and issubclass(exc_type, self._exc_cls)


__all__ = 'Supress',
