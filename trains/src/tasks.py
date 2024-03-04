from datetime import datetime
from random import choice

from src import app
from src.models.enums import EventType
from src.models.factories import TrainFactory
from src.models.models import STATIONS

train = TrainFactory()


@app.task
def broadcast_train_speed() -> dict:
    return {
        "created_at": datetime.now().isoformat(),
        "event_type": str(EventType.TRAIN_SPEED),
        "event_data": train.to_json(),
    }


@app.task
def broadcast_train_destinations() -> dict:
    train.destination = choice(STATIONS)
    return {
        "created_at": datetime.now().isoformat(),
        "event_type": str(EventType.TRAIN_DESTINATION),
        "event_data": train.to_json(),
    }
