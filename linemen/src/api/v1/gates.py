import logging
from http import HTTPStatus

from flask import Blueprint, abort, request
from src.models.models import GateState

logger = logging.getLogger("linemen")


bp = Blueprint("gates", __name__)

database = {}


@bp.route("/gates")
def get_gate_state() -> dict:
    logger.info("This is the gate-check endpoint")
    station = request.args.get("station")
    if station:
        gate = database.get(station)
        if gate:
            return {"state": str(gate.state)}
    abort(HTTPStatus.NOT_FOUND)


@bp.route("/gates/<station>/change-state", methods=["POST"])
def update_gate_state(station: str) -> dict:
    logger.info("This is the change-state endpoint")
    gate = database.get(station)
    if gate:
        new_state = GateState.CLOSED
        if gate.state == GateState.CLOSED:
            new_state = GateState.OPENED
        gate.state = new_state
        return {"state": str(gate.state)}
    abort(HTTPStatus.NOT_FOUND)
