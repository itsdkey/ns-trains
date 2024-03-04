import factory
from factory.fuzzy import FuzzyDecimal
from src.models.models import Station, Train


class StationFactory(factory.Factory):
    class Meta:
        model = Station

    name = factory.Faker("city")


class TrainFactory(factory.Factory):
    class Meta:
        model = Train

    destination = factory.SubFactory("src.models.factories.StationFactory")
    id = factory.Faker("uuid4")
    speed = FuzzyDecimal(0.0, 180.0)
