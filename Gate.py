from typing import List
from GateType import GateType
    

class Gate:
    def __init__(self, gateId, gateType: GateType):
        self.inputs: List[int] = []
        self.outputs: List[int] = []
        self.gates: List[Gate] = []
        self.gateType = gateType
        self.id = gateId


