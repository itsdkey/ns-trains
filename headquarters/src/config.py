class BaseConfig:
    """Base config for all configs.

    THIS SHOULD NOT BE USED AS A CONFIGURATION, PLEASE INHERIT THIS AND USE THE
    SUBCLASS.
    """

    FLASK_ENV = "development"
    TESTING = False


class StagingConfig(BaseConfig):
    """Config for staging environment."""

    FLASK_ENV = "staging"


class TestingConfig(BaseConfig):
    """Config for running tests on a separate 'clean' database."""

    TESTING = True
