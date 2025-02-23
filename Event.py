from enum import Enum, auto


class EventType(Enum):
    CIRCUIT_INPUT = auto()
    CIRCUIT_OUTPUT = auto()
    GATE = auto()
    LINK = auto()
    STATE_CHANGE = auto()
    STATE_VERIFY = auto()

    CLEAR = auto()
    QUIT = auto()
    RESET_SCALE = auto()

class Event:
    def __init__(self, eventType: EventType, payload=None):
        self.type = eventType
        self.payload = payload

class EventBus:
    def __init__(self):
        self.subscribers = [] 

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    def publish(self, event: Event):
        for subscriber in self.subscribers:
            subscriber.handleEvent(event)



