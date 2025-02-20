from typing import List
from GateType import GateType
    

class Gate:
    def __init__(self, gateId, gateType: GateType, numInputs, numOutputs):
        self.objects = {}
        self.type = gateType
        self.id = gateId
        self.numInputs = numInputs
        self.numOutputs = numOutputs


