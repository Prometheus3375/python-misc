from collections.abc import Callable, Iterator, Sequence
from contextlib import contextmanager
from functools import wraps
from time import perf_counter
from types import TracebackType
from typing import Any, NamedTuple, Self, final, overload, override

DURATION_UNIT_NAMES = 'yr', 'mo', 'wk', 'd', 'h', 'm', 's', 'ms', '	μs', 'ns'
DURATION_UNITS = {
    'years':        60 * 60 * 24 * 365,
    'months':       60 * 60 * 24 * 30,
    'weeks':        60 * 60 * 24 * 7,
    'days':         60 * 60 * 24,
    'hours':        60 * 60,
    'minutes':      60,
    'seconds':      1,
    'milliseconds': 10 ** -3,
    'microseconds': 10 ** -6,
    'nanoseconds':  10 ** -9,
    }


def _generate_non_zero_units[T](values: Sequence[T], /) -> Iterator[tuple[T, str]]:
    it = zip(values, DURATION_UNIT_NAMES)
    for value_unit in it:
        if value_unit[0] != 0:
            yield value_unit
            yield from it
            break
    else:
        # The iterator is exhausted, i.e., all values are zero,
        # yield the very last value with its unit.
        yield values[-1], DURATION_UNIT_NAMES[-1]


def format_seconds(seconds: float, /) -> str:
    """
    Formats the given number of seconds into
    years, months, weeks, days, hours, minutes, seconds,
    milliseconds, microseconds and nanoseconds.

    Identical to ``str(DurationData.from_seconds(seconds))``, but faster.
    """
    data = []
    for mul in DURATION_UNITS.values():
        value, seconds = divmod(seconds, mul)
        data.append(round(value))

    return ' '.join(
        f'{value}{unit}'
        for value, unit in _generate_non_zero_units(data)
        )


DEFAULT_MESSAGE_FORMAT = 'Time elapsed: {}'
"""
Default message format for time logging.
"""
DEFAULT_LOG_FUNCTION = print
"""
Default function for time logging.
"""


@contextmanager
def time_tracker(
        msg_fmt: str = DEFAULT_MESSAGE_FORMAT,
        log: Callable[[str], None] = DEFAULT_LOG_FUNCTION,
        ) -> Iterator[None]:
    """
    A context manager to track time of the underlined block of code.
    Whether the block fails or succeeds, the time is logged.

    :param msg_fmt: The format of the logged string,
      must contain one positional format parameter for the time entry.
    :param log: The callable for logging the message with the time entry in the given format.
    """
    start_time = perf_counter()
    try:
        yield
    finally:
        log(msg_fmt.format(format_seconds(perf_counter() - start_time)))


@overload
def track_time[** P, R](
        func: Callable[P, R],
        /,
        *,
        msg_fmt: str = DEFAULT_MESSAGE_FORMAT,
        log: Callable[[str], None] = DEFAULT_LOG_FUNCTION,
        ) -> Callable[P, R]: ...


@overload
def track_time[** P, R](
        func: None = None,
        /,
        *,
        msg_fmt: str = DEFAULT_MESSAGE_FORMAT,
        log: Callable[[str], None] = DEFAULT_LOG_FUNCTION,
        ) -> Callable[[Callable[P, R]], Callable[P, R]]: ...


def track_time[** P, R](
        func: Callable[P, R] | None = None,
        /,
        *,
        msg_fmt: str = DEFAULT_MESSAGE_FORMAT,
        log: Callable[[str], None] = DEFAULT_LOG_FUNCTION,
        ) -> Callable[P, R] | Callable[[Callable[P, R]], Callable[P, R]]:
    """
    A decorator that tracks time of the decorated function.
    Whether a function call fails or succeeds, the time is logged.

    :param func: A function to decorate.
      Can be omitted when other parameters specified and
      this decorator is used via special decorator syntax
    :param msg_fmt: The format of the logged string,
      must contain one positional format parameter for the time entry.
    :param log: The callable for logging the message with the time entry in the given format.
    """
    def decorator(func: Callable[P, R], /) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            start_time = perf_counter()
            try:
                return func(*args, **kwargs)
            finally:
                log(msg_fmt.format(format_seconds(perf_counter() - start_time)))

        return wrapper

    return decorator if func is None else decorator(func)


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
