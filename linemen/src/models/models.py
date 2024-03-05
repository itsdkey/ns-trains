from sqlalchemy import Enum
from src.db import db
from src.models.enums import GateState


class Gate(db.Model):
    station = db.Column(db.String(64), primary_key=True)
    state = db.Column(Enum(GateState))
