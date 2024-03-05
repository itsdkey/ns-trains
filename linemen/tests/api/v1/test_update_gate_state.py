from http import HTTPStatus

from flask import Flask
from flask.testing import FlaskClient
from src.db import db
from src.models.factories import GateFactory
from src.models.models import GateState


def test_update_returns_new_gates_state(app: Flask, client: FlaskClient):
    with app.app_context():
        gate = GateFactory(state=GateState.OPENED)
        db.session.commit()
        url = f"/gates/{gate.station}/change-state"
    expected_data = {"state": str(GateState.CLOSED)}

    response = client.post(url)

    assert response.status_code == HTTPStatus.OK
    assert response.json == expected_data


def test_update_returns_not_found_when_no_gate_found(client: FlaskClient):
    url = "/gates/random/change-state"

    response = client.post(url)

    assert response.status_code == HTTPStatus.NOT_FOUND
