from dataclasses import dataclass
from enum import Enum

from dataclasses_json import Undefined, dataclass_json


class GateState(Enum):
    OPENED = "OPENED"
    CLOSED = "PENDING"

    def __str__(self):
        return "%s" % self.value


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Gate:
    state: GateState
