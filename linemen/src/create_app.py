import os
from logging.config import fileConfig

from flask import Flask
from src.api.v1 import gates, info
from src.db import db, migrate
from werkzeug.utils import import_string


def create_app(config: str = None) -> Flask:
    config = config or os.getenv("FLASK_CONFIG", "StagingConfig")
    cfg = import_string(f"src.configs.{config}")()

    fileConfig("logging.ini")

    flask_app = Flask(__name__, instance_relative_config=True)
    flask_app.config.from_object(cfg)

    db.init_app(flask_app)
    migrate.init_app(flask_app, db)

    flask_app.register_blueprint(info.bp, url_prefix="/")
    flask_app.register_blueprint(gates.bp, url_prefix="/")

    return flask_app
