from random import choice

from flask import Blueprint
from src.db import db
from src.models.models import Gate, GateState

bp = Blueprint("commands", __name__, cli_group=None)


@bp.cli.command("init-db")
def init_db():
    stations = [
        "Białystok",
        "Białystok Bacieczki",
        "Białystok Elektrociepłownia",
        "Białystok Fabryczny",
        "Białystok GT",
        "Białystok Nowe Miasto",
        "Białystok R1",
        "Białystok R126",
        "Białystok R192",
        "Białystok R32",
        "Białystok R41",
        "Białystok R601",
        "Białystok R603",
        "Białystok R606",
        "Białystok Station",
        "Białystok Starosielce",
    ]
    states = [GateState.OPENED, GateState.CLOSED]
    for station in stations:
        gate = Gate(station=station, state=choice(states))
        db.session.add(gate)
    db.session.commit()
