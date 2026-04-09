# -*- coding: utf-8 -*-
import logging
import os
import weakref
import BigWorld

__all__ = [
    'logger',
    'byteify',
    'override',
    'overrideIn',
    'restore_overrides',
    'cancelCallbackSafe',
    'weak_callback'
]

logger = logging.getLogger('DispersionReticle')
logger.setLevel(logging.DEBUG if os.path.isfile('.debug_mods') else logging.ERROR)


def byteify(data):
    try:
        _unicode = unicode
    except NameError:
        _unicode = str

    if isinstance(data, dict):
        try:
            items = data.iteritems()
        except AttributeError:
            items = data.items()
        return {byteify(key): byteify(value) for key, value in items}
    elif isinstance(data, (list, tuple)):
        return [byteify(element) for element in data]
    elif isinstance(data, set):
        return {byteify(element) for element in data}
    elif isinstance(data, _unicode):
        return data.encode('utf-8')
    return data


_overrides = []


def override(holder, name, wrapper=None, setter=None):
    import types

    if wrapper is None:
        return lambda wrapper, setter=None: override(holder, name, wrapper, setter)

    target = getattr(holder, name)
    _overrides.append((holder, name, target))

    wrapped = lambda *a, **kw: wrapper(target, *a, **kw)

    if not isinstance(holder, types.ModuleType) and isinstance(target, types.FunctionType):
        setattr(holder, name, staticmethod(wrapped))
    elif isinstance(target, property):
        prop_getter = lambda *a, **kw: wrapper(target.fget, *a, **kw)
        prop_setter = (lambda *a, **kw: setter(target.fset, *a, **kw)) if setter else target.fset
        setattr(holder, name, property(prop_getter, prop_setter, target.fdel))
    else:
        setattr(holder, name, wrapped)


def overrideIn(cls, condition=None):
    def _wrap(func):
        if condition is not None and not condition():
            return func
        funcName = func.__name__
        if funcName.startswith('__') and not funcName.endswith('__'):
            funcName = '_' + cls.__name__ + funcName
        old = getattr(cls, funcName)
        _overrides.append((cls, funcName, old))
        def wrapper(*args, **kwargs):
            return func(old, *args, **kwargs)
        setattr(cls, funcName, wrapper)
        return wrapper
    return _wrap


def restore_overrides():
    while _overrides:
        holder, name, original = _overrides.pop()
        try:
            setattr(holder, name, original)
        except Exception:
            pass


def cancelCallbackSafe(cbid):
    try:
        if cbid is not None:
            BigWorld.cancelCallback(cbid)
            return True
    except (AttributeError, ValueError):
        pass
    return False


def weak_callback(obj, method_name, *args):
    ref = weakref.ref(obj)
    def _cb():
        instance = ref()
        if instance is not None:
            getattr(instance, method_name)(*args)
    return _cb
