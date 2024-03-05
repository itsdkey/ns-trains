from http import HTTPStatus

from flask import Flask
from flask.testing import FlaskClient
from src.db import db
from src.models.factories import GateFactory

URL_PATH = "/gates"


def test_get_returns_gates_state(app: Flask, client: FlaskClient):
    with app.app_context():
        gate = GateFactory()
        db.session.commit()
        data = {"station": gate.station}
        expected_data = {"state": str(gate.state)}

    response = client.get(URL_PATH, query_string=data)

    assert response.status_code == HTTPStatus.OK
    assert response.json == expected_data


def test_get_returns_not_found_when_no_gate_found(client: FlaskClient):
    data = {"station": "random"}

    response = client.get(URL_PATH, query_string=data)

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_get_returns_not_found_when_no_station_param(client: FlaskClient):
    response = client.get(URL_PATH)

    assert response.status_code == HTTPStatus.NOT_FOUND
