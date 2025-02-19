from enum import Enum, auto


class ButtonType(Enum):
    ADD_INPUT = auto()
    ADD_OUTPUT = auto()
    ADD_NOT_GATE = auto()
    ADD_AND_GATE = auto()
    ADD_NAND_GATE = auto()
    ADD_OR_GATE = auto()
    ADD_XOR_GATE = auto()
    ADD_NOR_GATE = auto()
    ADD_XNOR_GATE = auto()


