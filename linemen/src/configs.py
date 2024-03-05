import os


class BaseConfig:
    """Base config for all configs.

    THIS SHOULD NOT BE USED AS A CONFIGURATION, PLEASE INHERIT THIS AND USE THE
    SUBCLASS.
    """

    FLASK_ENV = "development"
    TESTING = False

    @property
    def SQLALCHEMY_DATABASE_URI(self):  # pragma: no cover
        if not (uri := os.getenv("SQLALCHEMY_DATABASE_URI")):
            user = os.getenv("POSTGRES_USER")
            password = os.getenv("POSTGRES_PASSWORD")
            db = os.getenv("POSTGRES_DB")
            host = os.getenv("POSTGRES_HOST")
            port = os.getenv("POSTGRES_PORT")
            uri = f"postgresql://{user}:{password}@{host}:{port}/{db}"
        return uri


class StagingConfig(BaseConfig):
    """Config for staging environment."""

    FLASK_ENV = "staging"


class TestingConfig(BaseConfig):
    """Config for running tests on a separate 'clean' database."""

    TESTING = True
