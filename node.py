from enum import Enum, auto


class NodeType(Enum):
    INPUT = auto()
    OUTPUT = auto()


class Node:
    def __init__(self, t: NodeType, state: int):
        self.t = t
        self.state = state


