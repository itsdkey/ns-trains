import factory
from factory.fuzzy import FuzzyChoice
from src.db import db
from src.models.models import Gate, GateState


class GateFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Gate
        sqlalchemy_session = db.session
        sqlalchemy_get_or_create = ("station",)

    station = factory.Faker("city")
    state = FuzzyChoice(GateState)
