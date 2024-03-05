from decimal import Decimal
from unittest import TestCase

from src.dataclasses import TrainSpeedEvent
from src.factories import TrainSpeedEventFactory
from src.tasks import process_train_speed


class TestProcessTrainSpeed(TestCase):

    def setUp(self) -> None:
        self.task = process_train_speed

    @staticmethod
    def _prepare_speed_event(event: TrainSpeedEvent) -> dict:
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
                event = TrainSpeedEventFactory(event_data__speed=speed)
                expected_messages = [
                    f"INFO:{log_name}:train: {event.event_data.id}, "
                    f"speed: {event.event_data.speed}",
                ]
                with self.assertLogs(log_name) as cm:

                    self.task(self._prepare_speed_event(event))

                    self.assertEqual(cm.output, expected_messages)
