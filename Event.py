from enum import Enum, auto


class EventType(Enum):
    ADD_INPUT_MODEL = auto()
    ADD_INPUT_VIEW = auto()
    ADD_OUTPUT_MODEL = auto()
    ADD_OUTPUT_VIEW = auto()
    ADD_NOT_GATE_MODEL = auto()
    ADD_NOT_GATE_VIEW = auto()
    ADD_AND_GATE_MODEL = auto()
    ADD_AND_GATE_VIEW = auto()
    ADD_NAND_GATE_MODEL = auto()
    ADD_NAND_GATE_VIEW = auto()
    ADD_OR_GATE_MODEL = auto()
    ADD_OR_GATE_VIEW = auto()
    ADD_XOR_GATE_MODEL = auto()
    ADD_XOR_GATE_VIEW = auto()
    ADD_NOR_GATE_MODEL = auto()
    ADD_NOR_GATE_VIEW = auto()
    ADD_XNOR_GATE_MODEL = auto()
    ADD_XNOR_GATE_VIEW = auto()


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



