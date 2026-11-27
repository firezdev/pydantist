# pydantist

[![AI-DECLARATION: assist](https://img.shields.io/badge/䷼%20AI--DECLARATION-assist-fef9c3?labelColor=fef9c3)](https://ai-declaration.md)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![PyPI](https://img.shields.io/pypi/v/pydantist)](https://pypi.org/project/pydantist/)
![Downloads](https://img.shields.io/pypi/dm/pydantist)

Lightweight and dependency-free alternative to pydantic.

```py
from pydantist import DantistModel

class User(DantistModel):
    name: str
    age: int
    active: bool

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
        self.active = True


user = User('Foo', 30)
print(user.name)  # Foo
print(user.age)  # 30
print(user.active)  # True

user = User.from_dict({'name': 'Bar', 'age': '67', 'active': 'no'})
print(user.name)  # Bar
print(user.age)  # 67
print(user.active)  # False
```

## Key features
 - Set your own **`__init__`** - pydantist doesn't touch it
 - Typed containers - `list[int]` / `dict[str, float]`, nested like `list[list[int]]`
 - Custom converters registry - you can easily add your own type
 - Lightweight and zero dependencies - whole lib size is less than 10 KB

## Custom converters

```py
from pydantist import DantistModel, register_converter


class RGB:
    def __init__(self, r: int, g: int, b: int):
        self.r, self.g, self.b = r, g, b
    
    @classmethod
    def from_hex(cls, value: str) -> "RGB":
        value = value.removeprefix("#")
        return cls(*(int(value[i:i + 2], 16) for i in (0, 2, 4)))

register_converter(str, RGB, RGB.from_hex)

class Theme(DantistModel):
    background: RGB

theme = Theme.from_dict({"background": "#1e1e2e"})
print(theme.background.r)  # 30
```

To allow format subclasses with your converter, pass `subclasses=True`:
```py
class RGBA(RGB):
    def __init__(self, r: int, g: int, b: int, a: int):
        super().__init__(r, g, b)
        self.a = a

    @classmethod
    def from_hex(cls, value: str) -> "RGB":
        value = value.removeprefix("#")
        return cls(*(int(value[i:i + 2], 16) for i in (0, 2, 4, 6)))


register_converter(str, RGB, lambda value, target_type: target_type.from_hex(value), subclasses=True)

class Theme(DantistModel):
    background: RGB
    overlay: RGBA

theme = Theme.from_dict({"background": "#1e1e2e", "overlay": "#00000080"})
print(theme.overlay.a)  # 128
print(theme.background.r)  # 30
```

## Installation
Requires Python 3.11+.

### uv
```bash
uv add pydantist
```

### pip
```bash
pip install pydantist
```

## Roadmap
 - [ ] `to_dict`
 - [ ] Custom field validators/serializers (like pydantic)
 - [ ] Format modes (strict/lossy)
 - [ ] Extended and meaningful exceptions
