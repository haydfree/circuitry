from typing import List

class Gate:
    def __init__(self):
        self.inputs: List[int] = []
        self.outputs: List[int] = []
        self.gates: List[Gate] = []
