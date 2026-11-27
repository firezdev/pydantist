from typing import Any


class UnparseableError(ValueError):
    def __init__(self, src: Any, typ: type):
        self.src = src
        self.typ = typ

    def __str__(self):
        return f"Unable to parse {self.src!r} as {self.typ.__name__ if isinstance(self.typ, type) else str(self.typ)}"
