
"""Types and meta classes"""


from types import FunctionType, UnboundMethodType
from application.python.decorator import preserve_signature


__all__ = 'Singleton', 'NullType', 'MarkerType'


class Singleton(type):
    """Metaclass for making singletons"""

    # noinspection PyInitNewSignature
    def __init__(cls, name, bases, dictionary):
        if type(cls.__init__) is UnboundMethodType:
            initializer = cls.__init__
        elif type(cls.__new__) is FunctionType:
            initializer = cls.__new__
        else:
            # noinspection PyUnusedLocal
            def initializer(self, *args, **kw): pass

        # noinspection PyShadowingNames
        @preserve_signature(initializer)
        def instance_creator(cls, *args, **kw):
            key = (args, tuple(sorted(kw.items())))
            try:
                hash(key)
            except TypeError:
                raise TypeError(
                    'cannot have singletons for classes with unhashable arguments')
            if key not in cls.__instances__:
                cls.__instances__[key] = super(
                    Singleton, cls).__call__(*args, **kw)
            return cls.__instances__[key]

        super(Singleton, cls).__init__(name, bases, dictionary)
        cls.__instances__ = {}
        cls.__instantiate__ = instance_creator.__get__(
            cls, type(cls))  # bind instance_creator to cls

    def __call__(cls, *args, **kw):
        return cls.__instantiate__(*args, **kw)


class NullTypeMeta(type):
    # noinspection PyInitNewSignature
    def __init__(cls, name, bases, dic):
        super(NullTypeMeta, cls).__init__(name, bases, dic)
        cls.__instance__ = super(NullTypeMeta, cls).__call__()

    def __call__(cls, *args, **kw):
        return cls.__instance__


class NullType(object, metaclass=NullTypeMeta):
    """Instances of this class always and reliably "do nothing"."""
    __name__ = 'Null'

    def __init__(self, *args, **kw):
        pass

    def __call__(self, *args, **kw):
        return self

    def __reduce__(self):
        return self.__class__, (), None

    def __repr__(self):
        return self.__name__

    def __str__(self):
        return self.__name__

    def __len__(self):
        return 0

    def __bool__(self):
        return False

    def __eq__(self, other):
        return self is other

    def __ne__(self, other):
        return self is not other

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __getattr__(self, name):
        return self

    def __setattr__(self, name, value):
        pass

    def __delattr__(self, name):
        pass

    def __getitem__(self, key):
        return self

    def __setitem__(self, key, value):
        pass

    def __delitem__(self, key):
        pass

    def __get__(self, instance, owner):
        return self

    def __set__(self, instance, value):
        pass

    def __delete__(self, obj):
        pass

    def __contains__(self, item):
        return False

    def __iter__(self):
        return self

    def __next__(self):
        raise StopIteration


class MarkerType(type):
    """Metaclass for defining marker entities"""

    __boolean__ = False

    def __call__(cls, *args, **kw):
        return cls

    def __repr__(cls):
        return cls.__name__

    def __bool__(cls):
        return cls.__boolean__
