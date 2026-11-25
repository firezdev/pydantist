from pydantist.format import format_value


class DantistModel:
    @classmethod
    def from_dict(cls, data: dict):
        instance = cls.__new__(cls)

        for attribute, type in cls.__annotations__.items():
            setattr(instance, attribute, format_value(data[attribute], type))

        return instance
