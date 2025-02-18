from NodeType import NodeType


class OutputView:
    def __init__(self, pos, size, outputId, state):
        self.pos = pos
        self.size = size
        self.x, self.y = pos
        self.id = outputId
        self.state = state 
        self.rect = None
        self.type = NodeType.OUTPUT


