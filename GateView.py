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

        self.font: pygame.font = pygame.font.SysFont("Source Code Pro", self.textSize) 
        self.renderedText = self.font.render(text, True, self.textColor)
        self.rect = pygame.Rect(self.left, self.top, self.width, self.height)

        self.updatePos(screen, self.pos)

    def addInputs(self, inputId):
        x = self.left
        yOffset = self.height / (self.numInputs+1)
        for idx in range(0, self.numInputs):
            y = self.top + ((idx+1)*yOffset)
            pos = (x,y)
            self.inputs.append(InputView(pos, self.nodeSize, inputId, 0, self.nodeColor))

    def addOutputs(self, outputId):
        x = self.left + self.width
        yOffset = self.height / (self.numOutputs+1)
        for idx in range(0, self.numOutputs):
            y = self.top + ((idx+1)*yOffset)
            pos = (x,y)
            self.outputs.append(OutputView(pos, self.nodeSize, outputId, 0, self.nodeColor))

    def drawInputs(self):
        for inp in self.inputs:
            inp.rect = pygame.draw.circle(self.screen, inp.color, inp.pos, inp.size)

    def drawOutputs(self):
        for out in self.outputs:
            out.rect = pygame.draw.circle(self.screen, out.color, out.pos, out.size)

    def updatePos(self, screen, pos):
        self.pos = pos
        self.left, self.top = pos
        rtwidth = self.renderedText.get_width()        
        rtheight = self.renderedText.get_height()        
        dw = self.width - rtwidth
        dh = self.height - rtheight
        self.textPos = (self.left+dw/2, self.top+dh/2)
        self.rect.update(pos, (self.width, self.height)) 


