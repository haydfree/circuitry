import pygame
from Gate import GateType
from InputView import InputView
from OutputView import OutputView


class GateView:
    def __init__(self, pos, size, gateType, gateId, numInputs, numOutputs, color, textColor, screen, nodeColor, textSize):
        self.pos = pos
        self.size = size
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

        if gateType == GateType.NOT_GATE:
            self.text = "NOT GATE"
        
        if gateType == GateType.AND_GATE:
            self.text = "AND GATE"

        self.objects = {}

        self.font: pygame.font = pygame.font.SysFont("Source Code Pro", self.textSize) 
        self.renderedText = self.font.render(self.text, True, self.textColor)
        self.rect = pygame.Rect(self.left, self.top, self.width, self.height)

        self.updatePos(screen, self.pos)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.renderedText, self.textPos)

        for idx in self.objects.keys():
            obj = self.objects[idx]
            obj.rect = pygame.draw.circle(screen, self.nodeColor, obj.pos, self.nodeSize)

    def addInputs(self, inputIds):
        x = self.left
        yOffset = self.height / (self.numInputs+1)
        for idx, inputId in enumerate(inputIds):
            y = self.top + ((idx+1)*yOffset)
            pos = (x,y)
            newInputView = InputView(pos, self.nodeSize, inputId, 0, self.nodeColor)
            newInputView.x = x
            newInputView.y = y
            self.objects[newInputView.id] = newInputView

    def addOutputs(self, outputIds):
        x = self.left + self.width
        yOffset = self.height / (self.numOutputs+1)
        for idx, outputId in enumerate(outputIds): 
            y = self.top + ((idx+1)*yOffset)
            pos = (x,y)
            newOutputView = OutputView(pos, self.nodeSize, outputId, 0, self.nodeColor)
            newOutputView.x = x
            newOutputView.y = y
            self.objects[newOutputView.id] = newOutputView

    def updatePos(self, screen, pos):
        xOffset = self.left - pos[0]
        yOffset = self.top - pos[1]
        self.pos = pos
        self.left, self.top = pos
        rtwidth = self.renderedText.get_width()        
        rtheight = self.renderedText.get_height()        
        dw = self.width - rtwidth
        dh = self.height - rtheight
        self.textPos = (self.left+dw/2, self.top+dh/2)
        self.rect.update(pos, (self.width, self.height)) 

        for idx in self.objects.keys():
            node = self.objects[idx]
            node.x -= xOffset
            node.y -= yOffset
            node.pos = (node.x,node.y)
            #node.rect = pygame.draw.circle(screen, self.nodeColor, node.pos, node.size) ??????????? like why????
            #pygame is fucking trash for this bruh
            node.rect.update(node.pos, (node.size,node.size))


