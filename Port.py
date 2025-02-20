from enum import Enum, auto


class PortType(Enum):
    CIRCUIT_INPUT = auto()
    CIRCUIT_OUTPUT = auto()
    GATE_INPUT = auto()
    GATE_OUTPUT = auto()

class Port:
    def __init__(self, portId):
        self.id = inputId
        self.state = None 
        self.input = None
        self.output = None


