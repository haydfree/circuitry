import pygame
from Gate import GateType
from InputView import InputView
from OutputView import OutputView


class GateView:
    def __init__(self, pos, size, text, gateType, gateId, numInputs, numOutputs, color, textColor, screen, nodeColor, textSize):
        self.pos = pos
        self.size = size
        self.text = text
        self.textSize = textSize
        self.type = gateType
        self.id = gateId 
        self.left = pos[0]
        self.top = pos[1]
        self.width = size[0]
        self.height = size[1]
        self.numInputs = numInputs
        self.numOutputs = numOutputs
        self.rect = None
        self.color = color
        self.nodeColor = nodeColor
        self.textColor = textColor
        self.nodeSize = 10
        self.screen = screen

        self.inputs = []
        self.outputs = []

        for inp in range(0, numInputs):
            self.inputs.append(InputView((0,0), self.nodeSize, inp, 0, self.nodeColor))

        for out in range(0, numOutputs):
            self.outputs.append(OutputView((0,0), self.nodeSize, out, 0, self.nodeColor))

        self.font: pygame.font = pygame.font.SysFont("Source Code Pro", self.textSize) 
        self.renderedText = self.font.render(text, True, self.textColor)
        self.rect = pygame.Rect(self.left, self.top, self.width, self.height)

        self.updatePos(screen, self.pos)

    def drawInputs(self):
        x = self.left
        yOffset = self.height / (self.numInputs+1)
        for inp in self.inputs:
            y = self.top + ((inp.id+1)*yOffset)
            pos = (x,y)
            inp.rect = pygame.draw.circle(self.screen, inp.color, pos, self.nodeSize)

    def drawOutputs(self):
        x = self.left + self.width
        yOffset = self.height / (self.numOutputs+1)
        for out in self.outputs:
            y = self.top + ((out.id+1)*yOffset)
            pos = (x,y)
            out.rect = pygame.draw.circle(self.screen, out.color, pos, self.nodeSize)

    def updatePos(self, screen, pos):
        self.pos = pos
        self.left, self.top = pos
        rtwidth = self.renderedText.get_width()        
        rtheight = self.renderedText.get_height()        
        dw = self.width - rtwidth
        dh = self.height - rtheight
        self.textPos = (self.left+dw/2, self.top+dh/2)
        self.rect.update(pos, (self.width, self.height)) 


