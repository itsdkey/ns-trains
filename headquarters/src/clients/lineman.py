from __future__ import annotations

import logging
import os

from src.clients.base import BaseClient
from src.clients.exceptions import ClientRequestError
from src.dataclasses.linemans import Gate

logger = logging.getLogger("headquarters")


class LinemanClient(BaseClient):
    def __init__(self, domain: str = None, **kwargs) -> None:
        domain = domain or os.environ.get("LINEMAN_DOMAIN")
        super().__init__(domain, **kwargs)
        self.api_path = "api/v1.0"

    def get(self, path: str, data: dict) -> dict:
        uri = self._build_uri(path)
        response = self._get(uri, params=data)
        if not response.ok:
            raise ClientRequestError(f"Request was unsuccessful: {response.content}")
        return response.json()

    def post(self, path: str, data: dict = None) -> dict:
        uri = self._build_uri(path)
        response = self._post(uri, json=data, timeout=self.timeout)
        if not response.ok:
            raise ClientRequestError(f"Request was unsuccessful: {response.content}")
        if response.status_code == 204:
            return {}
        return response.json()

    def _build_uri(self, path: str) -> str:
        return f"{self.domain}/{self.api_path}{path}"

    def get_gate_state(self, station: str) -> Gate:
        resource = "/gates"
        data = {"station": station}
        data = self.get(resource, data)
        return Gate.from_dict(data)

    def change_gate_state(self, station: str) -> Gate:
        resource = f"/gates/{station}/change-state"
        data = self.post(resource)
        return Gate.from_dict(data)
