import pygame
from Gate import GateType


class GateView:
    def __init__(self, pos, size, text, gateType, gateId, numInputs, numOutputs, color, textColor):
        self.pos = pos
        self.size = size
        self.text = text
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
        self.textColor = textColor

        self.font: pygame.font = pygame.font.SysFont("Source Code Pro", 10) 
        self.renderedText = self.font.render(text, True, self.textColor)
        self.rect = pygame.Rect(self.left, self.top, self.width, self.height)

        self.updatePos(self.pos)

    def updatePos(self, pos):
        self.pos = pos
        self.left, self.top = pos
        rtwidth = self.renderedText.get_width()        
        rtheight = self.renderedText.get_height()        
        dw = self.width - rtwidth
        dh = self.height - rtheight
        self.textPos = (self.left+dw/2, self.top+dh/2)
        self.rect.update(pos, (self.width, self.height)) 


