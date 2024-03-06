from sqlalchemy import Enum
from src.db import BaseModel, db
from src.models.enums import GateState


class Gate(BaseModel):
    station = db.Column(db.String(64), unique=True)
    state = db.Column(Enum(GateState))
