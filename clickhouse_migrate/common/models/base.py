import dataclasses


@dataclasses.dataclass
class BaseDto:
    """
    Base class for DTO
    """

    def asdict(self) -> dict:
        return dataclasses.asdict(self)
