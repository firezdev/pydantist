from functools import cache
from typing import Self, get_type_hints

from pydantist.format import format_value


class DantistModel:
    @classmethod
    @cache
    def _type_hints(cls) -> dict:
        return get_type_hints(cls)

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        instance = cls.__new__(cls)

        for attribute, type in instance._type_hints().items():
            setattr(instance, attribute, format_value(data[attribute], type))

        return instance
