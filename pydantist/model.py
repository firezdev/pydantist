from typing import Self, get_type_hints

from pydantist.format import format_value


class DantistModel:
    @classmethod
    def from_dict(cls, data: dict) -> Self:
        instance = cls.__new__(cls)

        for attribute, type in get_type_hints(cls).items():
            setattr(instance, attribute, format_value(data[attribute], type))

        return instance
