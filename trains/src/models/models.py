from dataclasses import dataclass, field
from decimal import Decimal
from random import choice, random
from uuid import UUID, uuid4

STATIONS = [
    "Białystok",
    "Białystok Bacieczki",
    "Białystok Elektrociepłownia",
    "Białystok Fabryczny",
    "Białystok GT",
    "Białystok Nowe Miasto",
    "Białystok R1",
    "Białystok R126",
    "Białystok R192",
    "Białystok R32",
    "Białystok R41",
    "Białystok R601",
    "Białystok R603",
    "Białystok R606",
    "Białystok Station",
    "Białystok Starosielce",
]


@dataclass
class Train:
    id: UUID = field(default_factory=lambda: uuid4())
    destination: str = field(default_factory=lambda: choice(STATIONS))

    @property
    def speed(self) -> Decimal:
        speed = str(random() * 180)
        speed = Decimal(speed).quantize(Decimal("0.00"))
        return speed

    def to_json(self) -> dict:
        return {
            "destination": self.destination,
            "id": str(self.id),
            "speed": str(self.speed),
        }
