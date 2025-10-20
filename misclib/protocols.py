from typing import Protocol

__all__ = 'SupportsDunderLT', 'SupportsDunderGT', 'SupportsRichComparison'


class SupportsDunderLT[T](Protocol):
    def __lt__(self, other: T, /) -> bool: ...


class SupportsDunderGT[T](Protocol):
    def __gt__(self, other: T, /) -> bool: ...


type SupportsRichComparison[T] = SupportsDunderLT[T] | SupportsDunderGT[T]
