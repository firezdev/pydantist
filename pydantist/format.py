from functools import wraps
from inspect import signature
from typing import Any, Callable, TypeVar, Union, cast, get_args, get_origin

from pydantist.exceptions import UnparseableError

#               from       to    converter val  from   out
_registry: dict[type, dict[type, Callable[[Any, type], Any]]] = {}
_subclass_allowed: set[tuple[type, type]] = set()


def register(
    src: type,
    dst: type,
    fn: Callable[[Any], Any] | Callable[[Any, type], Any],
    *,
    subclasses: bool = False
) -> None:
    try:
        signature(fn).bind(None, None)

    except (ValueError, TypeError):
        fn = cast(Callable[[Any], Any], fn)

        @wraps(fn)
        def _fn(value, _):
            return fn(value)

    else:
        _fn = cast(Callable[[Any, type], Any], fn)

    _registry.setdefault(src, {})[dst] = _fn
    if subclasses:
        _subclass_allowed.add((src, dst))
    else:
        _subclass_allowed.discard((src, dst))


T = TypeVar("T")


def format_value(v: Any, dst: type[T]) -> T:
    """
    Convert v to dst type.

    If dst is Any or type(v) is dst, value will return unchanged.

    Converter search order:
        1. By exact pair.
        2. By nearest pair of MRO of src and dst. Converter must be registered with subclasses=True.
    """
    src = type(v)

    if dst is Any or src is dst:
        return v

    full_dst = dst
    dst = get_origin(dst) or dst  # only base type, e.g list instead list[int]

    if dst is Union:
        args = get_args(full_dst)
        if src in args or Any in args:
            return v

        for arg in args:
            try:
                return format_value(v, arg)
            except ValueError:
                continue

        raise UnparseableError(v, full_dst)

    if converter := _registry.get(src, {}).get(dst):
        return converter(v, full_dst)

    for src_mro in src.__mro__:
        # find converters for nearest src's mro
        if converters := _registry.get(src_mro):
            for dst_mro in dst.__mro__:
                # find converters for nearest dst's mro (from converters that converts type of src)
                # check is subclasses allowed in this converter
                if (src_mro, dst_mro) in _subclass_allowed and (
                    converter := converters.get(dst_mro)
                ):
                    return converter(v, full_dst)

    raise UnparseableError(v, full_dst)
