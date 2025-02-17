from enum import Enum, auto

class EventType(Enum):
    ADD_INPUT_INCOMPLETE = auto()
    ADD_INPUT_COMPLETE = auto()

class Event:
    def __init__(self, eventType: EventType, payload=None):
        self.type = eventType
        self.payload = payload


