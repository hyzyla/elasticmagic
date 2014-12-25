import inspect

import dateutil.parser

from .compat import text_type
from .collections import OrderedAttributes


def instantiate(typeobj, *args, **kwargs):
    if inspect.isclass(typeobj):
        return typeobj(*args, **kwargs)
    return typeobj


class Type(object):
    def __init__(self):
        self.doc_cls = None

    def to_python(self, value):
        return value

    def to_python_single(self, value):
        return self.to_python(value)

    def from_python(self, value):
        return value


class String(Type):
    def to_python(self, value):
        if value is None:
            return None
        return text_type(value)


class Byte(Type):
    MIN_VALUE = -(1 << 7)
    MAX_VALUE = (1 << 7) - 1

    def to_python(self, value):
        if value is None:
            return None
        return int(value)


class Short(Type):
    MIN_VALUE = -(1 << 15)
    MAX_VALUE = (1 << 15) - 1

    def to_python(self, value):
        if value is None:
            return None
        return int(value)


class Integer(Type):
    MIN_VALUE = -(1 << 31)
    MAX_VALUE = (1 << 31) - 1

    def to_python(self, value):
        if value is None:
            return None
        return int(value)


class Long(Type):
    MIN_VALUE = -(1 << 63)
    MAX_VALUE = (1 << 63) - 1

    def to_python(self, value):
        if value is None:
            return None
        return int(value)


class Float(Type):
    def to_python(self, value):
        if value is None:
            return None
        return float(value)


class Double(Type):
    def to_python(self, value):
        if value is None:
            return None
        return float(value)


class Date(Type):
    # def __init__(self, format=None):
    #     self.format = format

    def to_python(self, value):
        if value is None:
            return None
        return dateutil.parser.parse(value)


class Boolean(Type):
    def to_python(self, value):
        if value is None:
            return None
        elif value is False or value == 0 or value in ('false', 'F'):
            return False
        return True


class Binary(Type):
    def to_python(self, value):
        # TODO: decode base64
        return value


class Ip(Type):
    def to_python(self, value):
        return value


class Object(Type):
    def __init__(self, doc_cls):
        self.doc_cls = doc_cls

    def to_python(self, value):
        if value is None:
            return None
        if isinstance(value, self.doc_cls):
            return value
        return self.doc_cls(**value)

    def from_python(self, value):
        if value is None:
            return None
        if isinstance(value, self.doc_cls):
            return value.to_source()
        return value


class Nested(Object):
    pass


class List(Type):
    def __init__(self, sub_type):
        self.sub_type = instantiate(sub_type)

    @property
    def doc_cls(self):
        return self.sub_type.doc_cls

    def to_python(self, value):
        if value is None:
            return None
        if not isinstance(value, list):
            value = [value]
        return [self.sub_type.to_python(v) for v in value]

    def to_python_single(self, value):
        v = self.to_python(value)
        if v:
            return v[0]

    def from_python(self, value):
        if value is None:
            return None
        if not isinstance(value, list):
            value = [value]
        return [self.sub_type.from_python(v) for v in value]
