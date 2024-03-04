from unittest.mock import ANY

from src.models.factories import TrainFactory


def test_train_to_json_returns_train_details() -> None:
    train = TrainFactory()
    expected_data = {
        "destination": train.destination,
        "id": str(train.id),
        "speed": ANY,
    }

    result = train.to_json()

    assert result == expected_data
