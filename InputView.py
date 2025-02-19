from NodeType import NodeType


class InputView:
    def __init__(self, pos, size, inputId, state, color):
        self.pos = pos
        self.size = size
        self.x, self.y = pos
        self.id = inputId
        self.state = state 
        self.rect = None
        self.type = NodeType.INPUT
        self.color = color

        self.inputs = []
        self.outputs = []
        self.linkedInputCounter = 0
        self.linkedOutputCounter = 0



