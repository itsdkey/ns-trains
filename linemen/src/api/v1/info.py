import logging
import os

from flask import Blueprint
from src.version import __version__

logger = logging.getLogger("trains")


bp = Blueprint("info", __name__)


@bp.route("/health-check")
def health_check() -> dict:
    logger.info("This is the health-check endpoint")
    return {"status": "OK"}


@bp.route("/version")
def get_version() -> dict:
    logger.info("This is the version endpoint")
    return {
        "commit": os.getenv("LAST_COMMIT", "dummy"),
        "version": __version__,
    }
