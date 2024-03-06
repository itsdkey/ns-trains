from random import choice

from flask import Blueprint
from sqlalchemy.dialects.postgresql import insert
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
    gates = []
    for station in stations:
        gates.append({"station": station, "state": str(choice(states))})
    statement = insert(Gate).values(gates).return_defaults()
    statement = statement.on_conflict_do_nothing(index_elements=["station"])
    db.session.execute(statement)
    db.session.commit()
    print(f"Created {gates=}")
