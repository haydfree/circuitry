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


