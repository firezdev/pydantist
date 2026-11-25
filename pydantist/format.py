from enum import Enum
from typing import Any

from pydantist.exceptions import UnparseableError


def format_value(v: Any, typ: type):
    if isinstance(v, typ):
        return v

    elif typ is int and isinstance(v, (str, int, float, bool)):
        return int(v)

    elif typ is float and isinstance(v, (str, int, float, bool)):
        return float(v)

    elif typ is bool:
        if isinstance(v, str):
            if v.lower() in ("true", "t", "yes", "on", "+", "y", "1"):
                return True
            elif v.lower() in ("false", "f", "no", "off", "-", "n", "0"):
                return False

        elif isinstance(v, (float, int)):
            if v == 0:
                return False
            elif v == 1:
                return True

        elif isinstance(v, (list, dict)):
            return bool(v)

    elif issubclass(typ, Enum):
        return typ(v)

    elif typ is str:
        if isinstance(v, (int, float, list, dict, bool)):
            return str(v)

    raise UnparseableError(v, typ)
