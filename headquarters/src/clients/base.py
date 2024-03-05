import logging
from abc import ABC, abstractmethod

import requests
from requests import Response
from requests.exceptions import ConnectionError, SSLError, Timeout
from src.clients.exceptions import ClientError

logger = logging.getLogger(__name__)


class ClientInterface(ABC):
    """Interface to store methods that a client should implement."""

    @abstractmethod
    def _get(self, uri: str, **kwargs) -> Response: ...

    @abstractmethod
    def _post(self, uri: str, **kwargs) -> Response: ...


class BaseClient(ClientInterface):
    """Base client to inherit from when creating a new one."""

    def __init__(self, domain: str = None, **kwargs) -> None:
        self.domain = domain
        self.timeout = kwargs.get("timeout", 10)
        self.transport = kwargs.get("transport") or requests

    def _get(self, uri: str, **kwargs) -> Response:
        logger.debug("%s._get: %s, kwargs: %s", self.__class__.__name__, uri, kwargs)

        try:
            response = self.transport.get(uri, **kwargs)
        except (ConnectionError, SSLError, Timeout) as exc:
            raise ClientError(f"An error occurred while requesting {uri}") from exc
        logger.debug("Response (%s): %s", response.status_code, response.content)
        return response

    def _post(self, uri: str, **kwargs) -> Response:
        logger.debug("%s._post: %s, kwargs: %s", self.__class__.__name__, uri, kwargs)

        try:
            response = self.transport.post(uri, **kwargs)
        except (ConnectionError, SSLError, Timeout) as exc:
            raise ClientError(f"An error occurred while requesting {uri}") from exc
        logger.debug("Response (%s): %s", response.status_code, response.content)
        return response
