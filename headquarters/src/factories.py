import factory
from factory.fuzzy import FuzzyDecimal
from src.dataclasses import CeleryEvent, TrainInfo
from src.enums import EventType


class TrainInfoFactory(factory.Factory):
    class Meta:
        model = TrainInfo

    destination = factory.Faker("city")
    id = factory.Faker("uuid4")
    speed = FuzzyDecimal(0, 180)


class CeleryEventFactory(factory.Factory):
    class Meta:
        model = CeleryEvent

    created_at = factory.Faker("date_time")
    event_type = EventType.TRAIN_SPEED
    event_data = factory.SubFactory("src.factories.TrainInfoFactory")
