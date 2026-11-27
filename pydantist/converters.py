from datetime import date, datetime, time, timedelta
from json import loads
from math import isfinite
from typing import Any, get_args

from pydantist.format import format_value, register


def _str2bool(v: str):
    v = v.lower().strip()
    if v in ("true", "t", "yes", "on", "+", "y", "1"):
        return True
    elif v in ("false", "f", "no", "off", "-", "n", "0"):
        return False
    else:
        raise ValueError(f"not a boolean string: {v!r}")


def _list2list(v: list, dst):
    args = get_args(dst)
    if not args:
        return v

    item_type = args[0]
    if item_type is Any:
        return v

    return [format_value(x, item_type) for x in v]


def _str2list(v: str, dst):
    v = loads(v)
    if not isinstance(v, list):
        raise ValueError("value must be list")

    return _list2list(v, dst)


def _dict2dict(x: dict, dst):
    args = get_args(dst)
    if not args:
        return x

    key_type, value_type = args
    if key_type is Any and value_type is Any:
        return x

    return {
        format_value(k, key_type): format_value(v, value_type) for k, v in x.items()
    }


def _str2dict(x: str, dst):
    x = loads(x)
    if not isinstance(x, dict):
        raise ValueError("value must be dict")

    return _dict2dict(x, dst)


def _num2bool(x: int | float):
    if x == 0:
        return False
    elif x == 1:
        return True
    raise ValueError("value must be 0 or 1")


def _float2int(x: float):
    if int(x) == x:
        return int(x)
    raise ValueError("value must be whole integer")


def _num2time(x: int | float):
    if 0 <= x < 86400:
        return (datetime.min + timedelta(seconds=x)).time()
    raise ValueError("value must be between 0 and 86400")


def _num2datetime(v: float) -> datetime:
    if not isfinite(v):
        raise ValueError(f"timestamp must be a finite number, got {v!r}")

    while abs(v) > 2e10:
        v /= 1000

    return datetime.fromtimestamp(v)


def _num2date(v: float) -> date:
    return _num2datetime(v).date()


def register_builtin_converters():
    register(str, int, int)
    register(str, float, float)
    register(str, bool, _str2bool)
    register(str, list, _str2list)
    register(str, dict, _str2dict)
    register(str, bytes, lambda x: x.encode())
    register(str, datetime, datetime.fromisoformat)
    register(str, date, date.fromisoformat)
    register(str, time, time.fromisoformat)

    register(int, str, str)
    register(int, float, float)
    register(int, bool, _num2bool)
    register(int, datetime, _num2datetime)
    register(int, date, _num2date)
    register(int, time, _num2time)
    register(int, timedelta, lambda x: timedelta(seconds=x))

    register(bool, int, lambda x: 1 if x else 0)
    register(bool, float, lambda x: 1.0 if x else 0.0)
    register(bool, str, lambda x: "true" if x else "false")

    register(float, int, _float2int)
    register(float, str, str)
    register(float, bool, _num2bool)
    register(float, datetime, _num2datetime)
    register(float, date, _num2date)
    register(float, time, _num2time)
    register(float, timedelta, lambda x: timedelta(seconds=x))

    register(list, list, _list2list)

    register(dict, dict, _dict2dict)
