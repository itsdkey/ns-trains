from http import HTTPStatus
from unittest.mock import patch

from flask.testing import FlaskClient
from src.models.factories import GateFactory
from src.models.models import GateState

database = {}


@patch("src.api.v1.gates.database", new=database)
def test_update_returns_new_gates_state(client: FlaskClient):
    gate = GateFactory(state=GateState.OPENED)
    database[gate.station] = gate
    url = f"/gates/{gate.station}/change-state"
    expected_data = {"state": str(GateState.CLOSED)}

    response = client.post(url)

    assert response.status_code == HTTPStatus.OK
    assert response.json == expected_data


def test_update_returns_not_found_when_no_gate_found(client: FlaskClient):
    url = "/gates/random/change-state"

    response = client.post(url)

    assert response.status_code == HTTPStatus.NOT_FOUND
