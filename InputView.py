from NodeType import NodeType


class InputView:
    def __init__(self, pos, size, inputId, state):
        self.pos = pos
        self.size = size
        self.x, self.y = pos
        self.id = inputId
        self.state = state 
        self.rect = None
        self.type = NodeType.INPUT


