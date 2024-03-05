import logging
from decimal import Decimal
from time import sleep

from src import app
from src.clients.exceptions import ClientRequestError
from src.clients.lineman import LinemanClient
from src.dataclasses.events import CeleryEvent
from src.dataclasses.linemans import GateState

logger = logging.getLogger(__name__)


@app.task(name="process_speed")
def process_train_speed(event: dict) -> None:
    event: CeleryEvent = CeleryEvent.from_dict(event)

    train = event.event_data
    train_speed = train.speed
    logger_name = "fast"
    if Decimal("0") <= train_speed < Decimal("40"):
        logger_name = "slow"
    elif Decimal("40") <= train_speed < Decimal("140"):
        logger_name = "normal"

    logger = logging.getLogger(logger_name)
    logger.info("train: %s, speed: %s", train.id, train_speed)


@app.task(
    name="process_station",
    autoretry_for=(ClientRequestError,),
    retry_kwargs={"max_retries": 3},
    retry_backoff=True,
)
def process_train_station(event: dict):
    event: CeleryEvent = CeleryEvent.from_dict(event)

    train = event.event_data
    station = train.destination

    logger.info("station: %s, train: %s", station, train.id)

    client = LinemanClient()
    gate = client.get_gate_state(station)
    if gate.state == GateState.OPENED:
        logger.info("station: %s, Gate is opened. Closing gate...", station)
        client.change_gate_state(station)
    else:
        logger.info("station: %s, Gate is closed!", station)

    sleep(10)

    logger.info("station: %s, Opening gate...", station)
    client.change_gate_state(station)
