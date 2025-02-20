from typing import List
from enum import Enum, auto


class GateType(Enum):
    NOT_GATE = auto()
    AND_GATE = auto()
    NAND_GATE = auto()
    OR_GATE = auto()
    XOR_GATE = auto()
    NOR_GATE = auto()
    XNOR_GATE = auto()
    CUSTOM_GATE = auto()


class Gate:
    def __init__(self, gateId, gateType: GateType, numInputs, numOutputs):
        self.objects = {}
        self.type = gateType
        self.id = gateId
        self.numInputs = numInputs
        self.numOutputs = numOutputs


