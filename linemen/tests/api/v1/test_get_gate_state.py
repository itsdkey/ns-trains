from http import HTTPStatus
from unittest.mock import patch

from flask.testing import FlaskClient
from src.models.factories import GateFactory

URL_PATH = "/gates"

database = {}


@patch("src.api.v1.gates.database", new=database)
def test_get_returns_gates_state(client: FlaskClient):
    gate = GateFactory()
    database[gate.station] = gate
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
