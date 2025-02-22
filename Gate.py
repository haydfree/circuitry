import sys
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

        self.state = None
        self.inputIds = []
        self.outputIds = []

    def run(self):
        for idx in self.objects.keys():
            obj = self.objects[idx]
            assert obj.input is not None and obj.output is not None
            if obj.type == PortType.GATE_OUTPUT:
                self.outputIds.append(obj.id)
            elif obj.type == PortType.GATE_INPUT:
                self.inputIds.append(obj.id)
            else:
                sys.exit("should not be here")

        if self.gateType == GateType.NOT_GATE:
            assert len(self.inputIds) == self.numInputs == 1
            assert len(self.outputIds) == self.numOutputs == 1
        elif self.gateType == GateType.AND_GATE:
            assert len(self.inputIds) == self.numInputs == 2
            assert len(self.outputIds) == self.numOutputs == 1

            outputPort = self.objects[self.outputIds[0]]
            inputPort0 = self.objects[self.inputIds[0]]
            inputPort1 = self.objects[self.inputIds[1]]
            outputPort.state = inputPort0.state & inputPort1.state
            self.state = outputPort.state

            

            

