from dataclasses import dataclass
from enum import Enum


class GateState(Enum):
    OPENED = "OPENED"
    CLOSED = "CLOSED"

    def __str__(self):
        return "%s" % self.value


@dataclass
class Gate:
    state: GateState
    station: str
