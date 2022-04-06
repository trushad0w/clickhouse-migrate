import dataclasses
from enum import Enum


class StrEnum(str, Enum):
    """
    Base class for string enums
    """

    def __str__(self):
        return self.value


@dataclasses.dataclass
class BaseDto:
    """
    Base class for DTO
    """

    def asdict(self) -> dict:
        return dataclasses.asdict(self)

    @classmethod
    def make(cls, data: dict):
        fields_values = {}
        for field in dataclasses.fields(cls):
            if not isinstance(field.default, dataclasses._MISSING_TYPE):
                field_value = field.default
            elif not isinstance(field.default_factory, dataclasses._MISSING_TYPE):
                field_value = field.default_factory()
            else:
                field_value = None
            fields_values[field.name] = field_value
        input_data = {
            key: value for key, value in dict(data).items() if key in fields_values
        }
        return cls(**{**fields_values, **input_data})
