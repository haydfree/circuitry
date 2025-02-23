import pygame
from Gate import GateType
from Port import Port, PortType


class GateView:
    def __init__(self, pos, size, gateType, gateId, numInputs, numOutputs, color, textColor, screen, portColor, textSize):
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
        self.portColor = portColor
        self.textColor = textColor
        self.portSize = 10
        self.screen = screen
        self.mainColor = color
        self.hoverColor = (255,255,255)
        self.rect = pygame.Rect(self.left, self.top, self.width, self.height)
        self.textPos = 0,0
        self.renderedText = None
        self.font = None

        if gateType == GateType.NOT_GATE:
            self.text = "NOT"
        elif gateType == GateType.AND_GATE:
            self.text = "AND"
        elif gateType == GateType.NAND_GATE:
            self.text = "NAND"
        elif gateType == GateType.OR_GATE:
            self.text = "OR"
        elif gateType == GateType.NOR_GATE:
            self.text = "NOR"
        elif gateType == GateType.XOR_GATE:
            self.text = "XOR"
        elif gateType == GateType.XNOR_GATE:
            self.text = "XNOR"
        else:
            self.text = "69420"


        self.objects = {}

    def draw(self, screen):
        self.drawText(screen)
        self.drawGate(screen)
        self.drawPorts(screen)

    def drawGate(self, screen):
        self.rect = pygame.Rect(self.left, self.top, self.width, self.height)
        self.rect = pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.renderedText, self.textPos)

    def drawText(self, screen):
        self.font = pygame.font.SysFont("Source Code Pro", self.textSize) 
        self.renderedText = self.font.render(self.text, True, self.textColor)
        self.textX = self.left + (self.width - self.renderedText.get_width())/2
        self.textY = self.top + (self.height - self.renderedText.get_height())/2
        self.textPos = (self.textX, self.textY)
        screen.blit(self.renderedText, self.textPos)

    def drawPorts(self, screen):
        for idx in self.objects.keys():
            port = self.objects[idx]
            port.rect = pygame.draw.circle(screen, self.portColor, port.pos, port.size)

    def update(self, screen, pos, scale):
        self.updateGateSize(screen, scale)
        self.updateGatePos(screen, pos)
        self.updatePortSize(scale)
        self.updatePortPos()

    def updateGatePos(self, screen, pos):
        self.left = pos[0] 
        self.top = pos[1] 
        self.pos = (self.left, self.top)

    def updateGateSize(self, screen, scale):
        self.width *= scale
        self.height *= scale
        self.size = (self.width, self.height)
        self.textSize *= scale
        self.textSize = int(self.textSize)

    def updatePortPos(self):
        inCounter = 1
        outCounter = 1
        for idx in self.objects.keys():
            port = self.objects[idx]
            if port.type == PortType.GATE_INPUT:
                slope = self.height / (self.numInputs + 1)
                port.x = self.left - port.size
                port.y = self.top + (inCounter * slope)
                inCounter += 1
            elif port.type == PortType.GATE_OUTPUT:
                slope = self.height / (self.numOutputs + 1)
                port.x = self.left + port.size + self.width
                port.y = self.top + (outCounter * slope)
                outCounter += 1
            port.pos = (port.x, port.y)

    def updatePortSize(self, scale):
        self.portSize *= scale
        for idx in self.objects.keys():
            port = self.objects[idx]
            port.size = self.portSize
         

