from abc import ABC
from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID, uuid4


class BaseModel(ABC):
    def to_json(self) -> dict: ...


@dataclass
class Station(BaseModel):
    name: str

    def to_json(self) -> dict:
        return {"name": self.name}


@dataclass
class Train(BaseModel):
    destination: Station
    speed: Decimal = Decimal("0.0")
    id: UUID = field(default_factory=lambda: uuid4())

    def to_json(self) -> dict:
        return {
            "id": str(self.id),
            "speed": str(self.speed.quantize(Decimal("0.00"))),
        }
