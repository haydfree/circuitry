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
        self.oldColor = color

        if gateType == GateType.NOT_GATE:
            self.text = "NOT"
        elif gateType == GateType.AND_GATE:
            self.text = "AND"
        elif gateType == GateType.NAND_GATE:
            self.text = "NAND"
        elif gateType == GateType.NAND_GATE:
            self.text = "OR"
        elif gateType == GateType.NAND_GATE:
            self.text = "NOR"
        elif gateType == GateType.NAND_GATE:
            self.text = "XOR"
        elif gateType == GateType.NAND_GATE:
            self.text = "XNOR"
        else:
            self.text = "69420"


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
            obj.rect = pygame.draw.circle(screen, self.portColor, obj.pos, self.portSize)

    def centerGatePorts(self):
        xIn = self.left
        xOut = self.width + self.left
        slopeIn = self.height / (self.numInputs+1)
        slopeOut = self.height / (self.numOutputs+1)
        counterIn = 1
        counterOut = 1
        for idx in self.objects.keys():
            obj = self.objects[idx]
            if obj.type == PortType.GATE_INPUT:
                x = xIn
                y = self.top + slopeIn * counterIn
                obj.pos = x,y 
                obj.x = x
                obj.y = y
                counterIn+=1
            elif obj.type == PortType.GATE_OUTPUT:
                x = xOut
                y = self.top + slopeOut * counterOut
                obj.pos = x,y 
                obj.x = x
                obj.y = y
                counterOut+=1

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
            port = self.objects[idx]
            port.x -= xOffset
            port.y -= yOffset
            port.pos = (port.x,port.y)
            #port.rect = pygame.draw.circle(screen, self.portColor, port.pos, port.size) ??????????? like why????
            #pygame is fucking trash for this bruh
            port.rect.update(port.pos, (port.size,port.size))


