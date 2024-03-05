from http import HTTPStatus

from flask.testing import FlaskClient

URL_PATH = "/health-check"


def test_health_check_returns_status(client: FlaskClient):
    expected_data = {"status": "OK"}

    response = client.get(URL_PATH)

    assert response.status_code == HTTPStatus.OK
    assert response.json == expected_data
