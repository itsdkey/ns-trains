import factory
from factory.fuzzy import FuzzyChoice
from src.models.models import Gate, GateState


class GateFactory(factory.Factory):
    class Meta:
        model = Gate

    state = FuzzyChoice(GateState)
    station = factory.Faker("city")
