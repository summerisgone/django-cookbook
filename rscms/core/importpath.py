# -*- coding: utf-8 -*-

def importpath(path):
    """
    Import value by specified ``path``.
    Value can represent module, class, object, attribute or method.
    """
    result = None
    attrs = []
    parts = path.split('.')
    exception = None
    while parts:
        try:
            result = __import__('.'.join(parts), {}, {}, [''])
        except ImportError, e:
            if exception is None:
                exception = e
            attrs = parts[-1:] + attrs
            parts = parts[:-1]
        else:
            break
    for attr in attrs:
        try:
            result = getattr(result, attr)
        except (AttributeError, ValueError):
            if exception is None:
                raise ImportError(path)
            raise exception
    return result
