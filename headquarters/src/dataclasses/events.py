from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from dataclasses_json import Undefined, config, dataclass_json
from marshmallow import fields
from src.consts import DATETIME_FORMAT
from src.enums import EventType


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class TrainInfo:
    destination: str
    id: UUID
    speed: Decimal


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class CeleryEvent:
    created_at: datetime = field(
        metadata=config(
            encoder=lambda x: datetime.isoformat(x),
            decoder=lambda x: datetime.fromisoformat(x),
            mm_field=fields.DateTime(format=DATETIME_FORMAT),
        ),
    )
    event_type: EventType
    event_data: TrainInfo
