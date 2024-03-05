import logging
from decimal import Decimal

from src.celery import app
from src.dataclasses import TrainSpeedEvent


@app.task(name="process_speed")
def process_train_speed(event: dict) -> None:
    event: TrainSpeedEvent = TrainSpeedEvent.from_dict(event)

    train = event.event_data
    train_speed = train.speed
    logger_name = "fast"
    if Decimal("0") <= train_speed < Decimal("40"):
        logger_name = "slow"
    elif Decimal("40") <= train_speed < Decimal("140"):
        logger_name = "normal"
    logger = logging.getLogger(logger_name)

    logger.info("train: %s, speed: %s", train.id, train_speed)


@app.task(name="process_destination")
def process_train_destinations(): ...
