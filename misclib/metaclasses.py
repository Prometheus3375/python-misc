from typing import Any, Never, final
from weakref import WeakValueDictionary

bases2combined = WeakValueDictionary()
"""
Maps a tuple of base classes to the respective subclass.
"""


def combine(*classes: type) -> 'CombineMeta':
    """
    Creates a subclass of the given classes as an instance of :class:`CombineMeta`
    and caches the result.
    """
    # Original idea: https://stackoverflow.com/a/45873191

    # Usage of WeakValueDictionary is safe here.
    # A combined class is present in this dict as long as it is referenced somewhere else.
    # Once nothing else references such class,
    # it is popped from the dictionary removing its respective key.
    # That key can be the last reference to other combined classes
    # leading to cascading dictionary cleanup.
    # All in all, none of unused classes are present in the dictionary.

    # Order of base classes matters.
    # (A, B) and (B, A) are different base tuples which lead to different MRO.
    # Thus, combined classes of these bases are different too.
    existing = bases2combined.get(classes)
    if existing is None:
        cls_name = '@'.join(
            f'({cls.__qualname__})' if '@' in cls.__qualname__ else cls.__qualname__
            for cls in classes
            )
        cls = CombineMeta(cls_name, classes, {'__module__': None})
        bases2combined[classes] = existing = cls

    return existing


@final
class CombineMeta(type):
    """
    A metaclass that allows metaclass combination.

    >>> from misclib.metaclasses import CombineMeta
    >>> class MyMeta(type, metaclass=CombineMeta):
    ...     def __new__(cls, /, *args, **kwargs):
    ...         print('Success!')
    ...         return super().__new__(cls, *args, **kwargs)
    ...
    >>> class MyClass(metaclass=MyMeta): pass
    ...
    Success!
    >>> from abc import ABC
    >>> class MyAbstractSubclass(ABC, MyClass): pass  # doctest: +NORMALIZE_WHITESPACE
    ...
    Traceback (most recent call last):
        ...
    TypeError: metaclass conflict: the metaclass of a derived class must be
    a (non-strict) subclass of the metaclasses of all its bases
    >>> from abc import ABCMeta
    >>> ABCMeta is type(ABC)
    True
    >>> class MyAbstractSubclass(ABC, MyClass, metaclass=ABCMeta @ MyMeta): pass
    ...
    Success!

    Combination is done by subclassing both operands in the same order.

    >>> combo1 = ABCMeta @ MyMeta
    >>> combo1.__bases__
    (<class 'abc.ABCMeta'>, <class '__main__.MyMeta'>)
    >>> combo2 = MyMeta @ ABCMeta
    >>> combo2.__bases__
    (<class '__main__.MyMeta'>, <class 'abc.ABCMeta'>)

    Combination is cached for the same sequence of base classes.

    >>> combo3 = MyMeta @ ABCMeta
    >>> combo3 is combo2
    True

    If none of the metaclasses are instances of :class:`CombineMeta`,
    call static method ``new`` with the classes to combine them.
    The created subclass is an instance of :class:`CombineMeta`.

    >>> class MyMeta(type):
    ...     def __new__(cls, /, *args, **kwargs):
    ...         print('Success!')
    ...         return super.__new__(cls, *args, **kwargs)
    ...
    >>> combo = CombineMeta.new(MyMeta, ABCMeta)
    >>> combo.__bases__
    (<class '__main__.MyMeta'>, <class 'abc.ABCMeta'>)
    >>> type(combo)
    <class 'misclib.metaclasses.CombineMeta'>
    """
    @staticmethod
    def new(cls1: type, cls2: type, /, *classes: type) -> 'CombineMeta':
        """
        Creates a subclass of the given classes as an instance of :class:`CombineMeta`
        and caches the result.
        """
        return combine(cls1, cls2, *classes)

    def __matmul__(self, other: type, /) -> 'CombineMeta':
        return combine(self, other)

    def __rmatmul__(self, other: type, /) -> 'CombineMeta':
        return combine(other, self)

    def __init_subclass__(mcs, /) -> Never:
        raise TypeError(f'type {CombineMeta.__name__!r} is not an acceptable base type')


class Singleton(type, metaclass=CombineMeta):
    """
    A metaclass to limit the number of class instances to the one single instance.

    >>> from misclib.metaclasses import Singleton
    >>> class Event(metaclass=Singleton):
    ...     def __init__(self, /, name: str, duration: int) -> None:
    ...         self.name = name
    ...         self.duration = duration
    ...     def __repr__(self, /) -> str:
    ...         return f'{self.__class__.__name__}(name={self.name!r}, duration={self.duration})'
    ...
    >>> obj = Event(name='dinner', duration=3600)
    >>> obj
    Event(name='dinner', duration=3600)
    >>> obj is Event()
    True

    Neither ``__new__`` nor ``__init__`` are called again
    once a singleton class was instantiated.

    >>> Event(name='lunch', duration=1800)
    Event(name='dinner', duration=3600)
    >>> obj is Event(name='lunch', duration=1800)
    True

    If there is a need to reinitialize the instance,
    call method ``__init__`` manually.

    >>> Event().__init__(name='lunch', duration=1800)

    >>> obj
    Event(name='lunch', duration=1800)

    Note, that subclasses of singletons have their own instance.

    >>> class SubEvent(Event): pass
    ...
    >>> obj is not SubEvent(name='lunch', duration=1800)
    True
    """
    # Usage of WeakValueDict[cls, instance] requires class instances to support weak references,
    # which can be undesired with defined slots.
    # Usage of WeakKeyDict[cls, instance] is impossible
    # as instances always keep a reference to their class;
    # unused classes and their instance will be forever in RAM.
    # Thus, usage of an external dictionary is not an option.
    # The implementation below assigns __instance__ to None on class creation,
    # so cls.__instance__ always references the attribute of cls and not its superclasses.
    # Alternatively, cls.__dict__['__instance__'] can be used for the same purpose;
    # then assigning __instance__ at class creation is not required.
    # Finally, it is possible to use class address to store its instance;
    # for example f'__{id(cls)}'.
    # Such approach makes instance attribute private as well and also random at runtime.

    def __init__(
            cls,
            name: str,
            bases: tuple[type, ...],
            namespace: dict[str, Any],
            /,
            **kwargs,
            ) -> None:
        super().__init__(name, bases, namespace, **kwargs)
        cls.__instance__ = None

    def __call__[T](cls: type[T], /, *args, **kwargs) -> T:
        self = cls.__instance__
        if self is None:
            cls.__instance__ = self = super().__call__(*args, **kwargs)

        return self


class EmptySlotsByDefaults(type, metaclass=CombineMeta):
    """
    A metaclass that adds empty slots if they are not defined inside the namespace of a class.
    """
    def __new__(
            mcs,
            name: str,
            bases: tuple[type, ...],
            namespace: dict[str, Any],
            /,
            **kwargs,
            ):
        # Do not use setdefaut here, create tuple only on demand.
        if '__slots__' not in namespace:
            namespace['__slots__'] = ()

        return super().__new__(mcs, name, bases, namespace, **kwargs)


__all__ = 'CombineMeta', 'Singleton', 'EmptySlotsByDefaults'
