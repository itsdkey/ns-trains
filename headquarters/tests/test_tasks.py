import os
from decimal import Decimal
from unittest import TestCase
from unittest.mock import patch

import responses
from src.dataclasses.events import CeleryEvent
from src.dataclasses.linemans import GateState
from src.factories import CeleryEventFactory
from src.tasks import process_train_speed, process_train_station


class TestProcessTrainSpeed(TestCase):

    def setUp(self) -> None:
        self.task = process_train_speed

    @staticmethod
    def _prepare_speed_event(event: CeleryEvent) -> dict:
        return {
            "created_at": event.created_at.isoformat(),
            "event_type": str(event.event_type),
            "event_data": {
                "destination": event.event_data.destination,
                "id": event.event_data.id,
                "speed": str(event.event_data.speed.quantize(Decimal("0.00"))),
            },
        }

    def test_task_logs_train_to_proper_log(self):
        cases = {
            Decimal("0.00"): "slow",
            Decimal("20.00"): "slow",
            Decimal("40.00"): "normal",
            Decimal("70.00"): "normal",
            Decimal("140.00"): "fast",
            Decimal("150.00"): "fast",
            Decimal("180.00"): "fast",
        }
        for speed, log_name in cases.items():
            with self.subTest(speed=speed):
                event = CeleryEventFactory(event_data__speed=speed)
                expected_messages = [
                    f"INFO:{log_name}:train: {event.event_data.id}, "
                    f"speed: {event.event_data.speed}",
                ]
                with self.assertLogs(log_name) as cm:

                    self.task(self._prepare_speed_event(event))

                    self.assertEqual(cm.output, expected_messages)


class TestProcessTrainStation(TestCase):

    def setUp(self) -> None:
        self.task = process_train_station
        self.log_name = "headquarters"
        self.lineman_domain = os.environ.get("LINEMAN_DOMAIN")

        patch("src.tasks.sleep").start()
        self.m_responses = responses.RequestsMock()
        self.m_responses.start()

        self.addCleanup(patch.stopall)
        self.addCleanup(self.m_responses.reset)
        self.addCleanup(self.m_responses.stop)

    @staticmethod
    def _prepare_station_event(event: CeleryEvent) -> dict:
        return {
            "created_at": event.created_at.isoformat(),
            "event_type": str(event.event_type),
            "event_data": {
                "destination": event.event_data.destination,
                "id": event.event_data.id,
                "speed": str(event.event_data.speed.quantize(Decimal("0.00"))),
            },
        }

    def _mock_lineman_response(
        self, station: str, gate_state: GateState
    ) -> responses.BaseResponse:
        params = {"station": station}
        return self.m_responses.get(
            f"{self.lineman_domain}/api/v1.0/gates",
            status=200,
            json={"state": str(gate_state)},
            match=[responses.matchers.query_param_matcher(params)],
        )

    def test_task_logs_info_when_gate_is_closed(self):
        event = CeleryEventFactory()
        station = event.event_data.destination
        self._mock_lineman_response(station, GateState.CLOSED)
        self.m_responses.post(
            f"{self.lineman_domain}/api/v1.0/gates/{station}/change-state",
            status=200,
            json={"state": str(GateState.OPENED)},
        )
        expected_messages = [
            f"INFO:{self.log_name}:"
            f"station: {event.event_data.destination}, "
            f"train: {event.event_data.id}",
            f"INFO:{self.log_name}:"
            f"station: {event.event_data.destination}, "
            f"Gate is closed!",
            f"INFO:{self.log_name}:"
            f"station: {event.event_data.destination}, "
            f"Opening gate...",
        ]
        with self.assertLogs(self.log_name) as cm:

            self.task(self._prepare_station_event(event))

            self.assertEqual(cm.output, expected_messages)

    def test_task_logs_info_when_gate_is_opened(self):
        event = CeleryEventFactory()
        station = event.event_data.destination
        self._mock_lineman_response(station, GateState.OPENED)
        self.m_responses.post(
            f"{self.lineman_domain}/api/v1.0/gates/{station}/change-state",
            status=200,
            json={"state": str(GateState.CLOSED)},
        )
        expected_messages = [
            f"INFO:{self.log_name}:"
            f"station: {event.event_data.destination}, "
            f"train: {event.event_data.id}",
            f"INFO:{self.log_name}:"
            f"station: {event.event_data.destination}, "
            f"Gate is opened. Closing gate...",
            f"INFO:{self.log_name}:"
            f"station: {event.event_data.destination}, "
            f"Opening gate...",
        ]
        with self.assertLogs(self.log_name) as cm:

            self.task(self._prepare_station_event(event))

            self.assertEqual(cm.output, expected_messages)

    def test_task_calls_lineman_to_do_his_work_when_gate_is_opened(self):
        event = CeleryEventFactory()
        station = event.event_data.destination
        self._mock_lineman_response(station, GateState.OPENED)
        self.m_responses.post(
            f"{self.lineman_domain}/api/v1.0/gates/{station}/change-state",
            status=200,
            json={"state": str(GateState.CLOSED)},
        )
        self.m_responses.post(
            f"{self.lineman_domain}/api/v1.0/gates/{station}/change-state",
            status=200,
            json={"state": str(GateState.OPENED)},
        )

        result = self.task(self._prepare_station_event(event))

        self.assertIsNone(result)

    def test_task_calls_lineman_to_do_his_work_when_gate_is_closed(self):
        event = CeleryEventFactory()
        station = event.event_data.destination
        self._mock_lineman_response(station, GateState.CLOSED)
        self.m_responses.post(
            f"{self.lineman_domain}/api/v1.0/gates/{station}/change-state",
            status=200,
            json={"state": str(GateState.OPENED)},
        )

        result = self.task(self._prepare_station_event(event))

        self.assertIsNone(result)
