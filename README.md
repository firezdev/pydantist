# pydantist

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
print(user.name) # Foo
print(user.age) # 30
print(user.active) # True

user = User.from_dict({'name': 'Bar', 'age': '67', 'active': 'no'})
print(user.name) # Bar
print(user.age) # 67
print(user.active) # False
```

## Key features
 - Set your own **`__init__`** - pydantist don't touch it
 - Custom converters registry - you can easily add your own type

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
 - [ ] Custom field validators/serializiers (like pydantic)
 - [ ] Format modes (srtict/lossy)
 - [ ] Extended and meaningful exceptions
