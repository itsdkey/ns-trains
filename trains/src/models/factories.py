import factory
from factory.fuzzy import FuzzyChoice
from src.models.models import STATIONS, Train


class TrainFactory(factory.Factory):
    class Meta:
        model = Train

    destination = FuzzyChoice(STATIONS)
    id = factory.Faker("uuid4")
