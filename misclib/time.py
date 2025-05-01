from collections.abc import Callable
from functools import wraps
from itertools import dropwhile
from time import perf_counter
from types import TracebackType
from typing import Any, NamedTuple, Self, final

DURATION_UNIT_NAMES = 'yr', 'mo', 'wk', 'd', 'h', 'min', 's'
DURATION_UNITS = {
    'years':   60 * 60 * 24 * 365,
    'months':  60 * 60 * 24 * 30,
    'weeks':   60 * 60 * 24 * 7,
    'days':    60 * 60 * 24,
    'hours':   60 * 60,
    'minutes': 60,
    'seconds': 1,
    }


def _is_zero(value_unit: tuple[int, str], /) -> bool:
    return value_unit[0] == 0


class DurationData(NamedTuple):
    """
    Data structure representing duration information in different units.
    """
    years: int
    months: int
    weeks: int
    days: int
    hours: int
    minutes: int
    seconds: int

    @property
    def total(self, /) -> int:
        """
        The total duration in seconds.
        """
        return sum(
            value * mul
            for value, mul in zip(self, DURATION_UNITS.values())
            )

    @classmethod
    def from_seconds(cls, seconds: float, /) -> Self:
        """
        Creates an instance of :class:`DurationData` from
        the given floating point number of seconds.
        """
        s = round(seconds)
        data = {}
        for name, mul in DURATION_UNITS.items():
            data[name], s = divmod(s, mul)

        return cls(**data)

    def __format__(self, fmt: str, /) -> str:
        return ' '.join(
            f'{value:{fmt}}{unit}'
            for value, unit in dropwhile(_is_zero, zip(self, DURATION_UNIT_NAMES))
            )

    def __str__(self, /) -> str:
        return self.__format__('')


ZERO_DURATION = DurationData.from_seconds(0)
"""
Special instance of :class:`DurationData` representing zero duration.
"""


class TimeTracker:
    """
    Base class for context managers to track time of underlined block of code.

    Subclasses cannot overwrite methods ``__enter__`` and ``__exit__``,
    but can overwrite methods ``_enter``, ``_exit_success`` and ``_exit_exception``.
    """
    __slots__ = '__start_time', '_duration'

    def __init__(self, /) -> None:
        self.__start_time = 0.
        self._duration = ZERO_DURATION

    @property
    def duration(self, /) -> DurationData:
        """
        Execution time of the runtime context.

        If the context is not entered or is still running, returns zero duration.
        """
        return self._duration

    def _enter(self, /) -> None:
        """
        Actions performed upon entering the runtime context.

        Default implementation sets starting time and resets duration.
        """
        self.__start_time = perf_counter()
        self._duration = ZERO_DURATION

    @final
    def __enter__(self, /) -> Self:
        self._enter()
        return self

    def _exit_success(self, /) -> None:
        """
        Actions performed upon exiting the runtime context with no exceptions.

        Default implementation prints time elapsed.
        """
        print(f'\nTime elapsed: {self._duration}')

    # noinspection PyUnusedLocal
    def _exit_exception(self, exc: BaseException, traceback: TracebackType, /) -> None:
        """
        Actions performed upon exiting the runtime context with an exception.

        Default implementation prints time elapsed.
        """
        print(f'\nTime elapsed: {self._duration}')

    @final
    def __exit__(
            self,
            exc_type: type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None,
            /,
            ) -> bool:
        self._duration = DurationData.from_seconds(perf_counter() - self.__start_time)

        if exc_type is None:
            self._exit_success()
        else:
            self._exit_exception(exc_val, exc_tb)

        return False


def format_seconds(seconds: float, fmt: str = '', /) -> str:
    """
    Formats the given number of seconds similar to formatting of :class:`DurationData`.
    Identical to ``str(DurationData.from_seconds(seconds))``, but faster.
    """
    s = round(seconds)
    data = []
    for mul in DURATION_UNITS.values():
        value, s = divmod(s, mul)
        data.append(value)

    return ' '.join(
        f'{value:{fmt}}{unit}'
        for value, unit in dropwhile(_is_zero, zip(data, DURATION_UNIT_NAMES))
        )


def track_time[** P, R](func: Callable[P, R], /) -> Callable[P, R]:
    """
    A decorator that prints elapsed time after function call.
    """
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start_time = perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            print(f'\nTime elapsed: {format_seconds(perf_counter() - start_time)}')

    return wrapper


class CallableTimeTracker(TimeTracker):
    """
    A special time tracker for callable objects.
    Decorate a callable with method ``wrap`` to add time tracking for its every call.
    """
    __slots__ = '_call_str',

    def __init__(
            self,
            func: Callable,
            func_args: tuple,
            func_kwargs: dict[str, Any],
            /,
            ) -> None:
        super().__init__()

        args = [repr(v) for v in func_args]
        args.extend(f'{name}={v!r}' for name, v in func_kwargs.items())
        self._call_str = f'{func.__qualname__}({', '.join(args)})'

    def _exit_success(self, /) -> None:
        print(f'Call {self._call_str} successful, time elapsed: {self._duration}')

    # noinspection PyUnusedLocal
    def _exit_exception(self, exc: BaseException, traceback: TracebackType, /) -> None:
        print(
            f'Call {self._call_str} failed, '
            f'{type(exc)}: {str(exc)}\n'
            f'Time elapsed: {self._duration}'
            )

    @classmethod
    def wrap[** P, R](cls, callable_: Callable[P, R], /) -> Callable[P, R]:
        """
        Decorates the given callable with the instance of this class.
        """
        @wraps(callable_)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            with cls(callable_, args, kwargs):
                return callable_(*args, **kwargs)

        return wrapper


__all__ = (
    'DurationData',
    'ZERO_DURATION',
    'TimeTracker',
    'format_seconds',
    'track_time',
    'CallableTimeTracker',
    )
