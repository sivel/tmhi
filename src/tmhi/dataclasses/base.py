from dataclasses import MISSING
from dataclasses import dataclass
from dataclasses import fields


@dataclass(init=False, kw_only=True)
class TMHIDataClass:
    def __init__(self, **kwargs):
        field_names = set()
        no_defaults = set()
        for f in fields(self):
            field_names.add(f.name)
            if (source_name := f.metadata.get('name')):
                kwargs[f.name] = kwargs.pop(source_name)
            if f.default is MISSING:
                no_defaults.add(f.name)
        kwarg_names = set(kwargs.keys())
        if (bad := kwarg_names.difference(field_names)):
            raise TypeError(
                f'{self.__class__.__name__}.__init__() got an unexpected '
                f'keyword argument {bad.pop()!r}: {field_names=}'
            )
        if (missing := no_defaults.difference(kwarg_names)):
            raise TypeError(
                f'{self.__class__.__name__}.__init__() missing required '
                f'argument: {missing.pop()!r}'
            )
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.__post_init__()

    def __post_init__(self):
        for f in fields(self):
            value = getattr(self, f.name)
            if (converter := f.metadata.get('converter')):
                if callable(converter):
                    value = converter(value)
                else:
                    value = getattr(self, converter)(value)
            else:
                if value is None:
                    pass
                elif isinstance(value, dict):
                    value = f.type(**value)
                else:
                    value = f.type(value)
                if isinstance(value, list):
                    sub_type = f.type.__args__[0]
                    for i, v in enumerate(value):
                        if isinstance(v, dict):
                            value[i] = sub_type(**v)
                        else:
                            value[i] = sub_type(v)
            setattr(self, f.name, value)
