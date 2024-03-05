import os

import pytest
from flask import Flask
from flask.testing import FlaskClient, FlaskCliRunner
from src import create_app


@pytest.fixture()
def app():
    config_class = os.getenv("FLASK_CONFIG", "TestingConfig")
    app = create_app(config_class)

    # other setup can go here
    yield app
    # clean up / reset resources here


@pytest.fixture()
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@pytest.fixture()
def runner(app: Flask) -> FlaskCliRunner:
    return app.test_cli_runner()
