from datetime import datetime
from decimal import Decimal
from unittest import TestCase
from unittest.mock import PropertyMock, patch

from src.models.enums import EventType
from src.models.factories import TrainFactory
from src.models.models import STATIONS, Train
from src.tasks import broadcast_train_destinations, broadcast_train_speed


class TestBroadcastTrainSpeed(TestCase):

    def setUp(self) -> None:
        self.task = broadcast_train_speed

        self.train = TrainFactory()
        self.m_train = patch("src.tasks.train", new=self.train).start()
        type(self.m_train).speed = PropertyMock(return_value=Decimal("10.0"))
        self.addCleanup(patch.stopall)

    @staticmethod
    def _prepare_train_info(train: Train) -> dict:
        return {
            "destination": train.destination,
            "id": str(train.id),
            "speed": str(train.speed),
        }

    @patch("src.tasks.app.send_task")
    @patch("src.tasks.datetime")
    def test_task_sends_info_to_queue(self, m_datetime, m_send_task):
        today = datetime.now()
        m_datetime.now.return_value = today
        task_name = "process_speed"
        expected_data = {
            "created_at": today.isoformat(),
            "event_type": str(EventType.TRAIN_SPEED),
            "event_data": self._prepare_train_info(self.train),
        }

        result = self.task()

        self.assertIsNone(result)
        m_send_task.assert_called_once_with(task_name, args=[expected_data])


class TestBroadcastTrainDestination(TestCase):

    def setUp(self) -> None:
        self.task = broadcast_train_destinations

        self.train = TrainFactory()
        self.m_train = patch("src.tasks.train", new=self.train).start()
        type(self.m_train).speed = PropertyMock(return_value=Decimal("10.0"))
        self.addCleanup(patch.stopall)

    @staticmethod
    def _prepare_train_info(train: Train) -> dict:
        return {
            "destination": train.destination,
            "id": str(train.id),
            "speed": str(train.speed),
        }

    @patch("src.tasks.app.send_task")
    @patch("src.tasks.choice")
    @patch("src.tasks.datetime")
    def test_success(self, m_datetime, m_choice, m_send_task):
        new_destination = STATIONS[0]
        self.train.destination = m_choice.return_value = new_destination
        today = datetime.now()
        m_datetime.now.return_value = today
        task_name = "process_station"
        expected_data = {
            "created_at": today.isoformat(),
            "event_type": str(EventType.TRAIN_DESTINATION),
            "event_data": self._prepare_train_info(self.train),
        }

        result = self.task()

        self.assertIsNone(result)
        m_send_task.assert_called_once_with(task_name, args=[expected_data])
