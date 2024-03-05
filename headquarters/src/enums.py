from enum import Enum


class BaseEnum(Enum):
    def __str__(self):
        return "%s" % self.value.upper()


class EventType(BaseEnum):
    TRAIN_DESTINATION = "TRAIN_DESTINATION"
    TRAIN_SPEED = "TRAIN_SPEED"
