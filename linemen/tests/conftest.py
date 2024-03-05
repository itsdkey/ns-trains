import os

import pytest
from flask import Flask
from flask.testing import FlaskClient, FlaskCliRunner
from src.create_app import create_app
from src.db import db


@pytest.fixture()
def app():
    config_class = os.getenv("FLASK_CONFIG", "TestingConfig")
    app = create_app(config_class)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@pytest.fixture()
def runner(app: Flask) -> FlaskCliRunner:
    return app.test_cli_runner()
