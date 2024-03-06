import os
from datetime import datetime
from random import choice
from uuid import uuid4

from src import app
from src.models.enums import EventType
from src.models.factories import TrainFactory
from src.models.models import STATIONS

train = TrainFactory(id=os.getenv("TRAIN_ID", str(uuid4())))


@app.task(name="broadcast_train_speed")
def broadcast_train_speed() -> None:
    data = {
        "created_at": datetime.now().isoformat(),
        "event_type": str(EventType.TRAIN_SPEED),
        "event_data": train.to_json(),
    }
    app.send_task("process_speed", args=[data])


@app.task(name="broadcast_train_destinations")
def broadcast_train_destinations() -> None:
    train.destination = choice(STATIONS)
    data = {
        "created_at": datetime.now().isoformat(),
        "event_type": str(EventType.TRAIN_DESTINATION),
        "event_data": train.to_json(),
    }
    app.send_task("process_station", args=[data])
