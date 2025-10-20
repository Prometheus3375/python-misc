from collections.abc import Collection, Iterable
from traceback import format_tb


def format_exception(exc: BaseException, /) -> str:
    """
    Returns a string representation of the given exception with its full traceback.
    If the exception does not have any traceback, returns a string with exception type and message.
    """
    exc_name = exc.__class__.__qualname__
    exc_module = exc.__class__.__module__
    if exc_module is not None and exc_module != 'builtins':
        exc_name = f'{exc_module}.{exc_name}'

    tb_lines = format_tb(exc.__traceback__)
    if tb_lines:
        return f'Traceback (most recent call last):\n{''.join(tb_lines)}{exc_name}: {exc}'

    return f'{exc_name}: {exc}'


def truncate_string(value: str, limit: int = 10, /) -> str:
    """
    If the length of the given string is higher than the limit,
    cuts it to ``limit - 3`` characters and appends the ellipsis.
    Returns the string unchanged otherwise.
    """
    return f'{value[:limit - 3]}...' if len(value) > limit else value


def repr_collection[T: (str, Iterable[str])](
        c: Collection,
        singular: T,
        plural: T,
        /,
        *,
        delimiter: str = ', ',
        use_repr: bool = True,
        ) -> tuple[T, str]:
    """
    Represents the given collection and determines the appropriate noun to describe its elements.
    :param c: The collection to represent.
    :param singular: Noun or :class:`Iterable` of nouns
      describing a single element from the collection.
    :param plural: Noun or :class:`Iterable` of nouns
      describing multiple elements from the collection.
    :param delimiter: Separator between the elements of the collection
      in its string representation.
      Defaults to a comma with space after.
    :param use_repr: Whether to use function ``repr``
      for representing individual elements of the collection.
      If ``False``, function ``str`` is used instead.
      Defaults to ``True``.
    :return: A tuple of size 2.
      The first element is ``singular``
      if the collection contains one element and ``plural`` otherwise.
      The second element is the final string representation of the collection.
    """
    func = repr if use_repr else str
    return singular if len(c) == 1 else plural, delimiter.join(func(o) for o in c)


__all__ = 'format_exception', 'truncate_string', 'repr_collection'
