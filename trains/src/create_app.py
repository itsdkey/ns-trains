import os
from logging.config import fileConfig

from flask import Flask
from werkzeug.utils import import_string


def create_app(config: str = None) -> Flask:
    config = config or os.getenv("FLASK_CONFIG", "StagingConfig")
    cfg = import_string(f"src.config.{config}")()

    fileConfig("logging.ini")

    flask_app = Flask(__name__, instance_relative_config=True)
    flask_app.config.from_object(cfg)

    return flask_app
