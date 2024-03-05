from http import HTTPStatus
from unittest.mock import ANY

from flask.testing import FlaskClient
from src.version import __version__

URL_PATH = "/version"


def test_version_returns_version_information(client: FlaskClient):
    expected_data = {"commit": ANY, "version": __version__}

    response = client.get(URL_PATH)

    assert response.status_code == HTTPStatus.OK
    assert response.json == expected_data
