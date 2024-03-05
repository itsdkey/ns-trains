import logging
from decimal import Decimal

from src.celery import app
from src.dataclasses import CeleryEvent


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


@app.task(name="process_station")
def process_train_station(event: dict):
    event: CeleryEvent = CeleryEvent.from_dict(event)

    train = event.event_data

    logger = logging.getLogger("headquarters")
    logger.info("station: %s, train: %s", train.destination, train.id)
