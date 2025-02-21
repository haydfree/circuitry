import pygame
import pdb
from typing import Tuple
from Port import PortType
from Gate import GateType
from Event import EventType, Event, EventBus
from ButtonView import ButtonView, ButtonType
from GateView import GateView
from PortView import PortView


class View:
    def __init__(self, eventBus: EventBus, windowWidth: int, windowHeight: int):
        self.eventBus = eventBus

        pygame.init()
        self.screen: pygame.display = pygame.display.set_mode((windowWidth, windowHeight))
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.running: bool = True
        self.frameRate = 60
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight

        self.objects = {}

        self.buttonCounter = 0

        self.buttonTextColor = pygame.Color(200, 200, 200)
        self.backgroundColor = pygame.Color(40,28,52)
        self.buttonColor = pygame.Color(50, 50, 50)
        self.portColor = pygame.Color(20, 20, 20)
        self.buttonSize = (80, 50)
        self.buttonTextSize = 10
        self.portSize = 10
        self.menuHeight = 100
        self.portMargin = 50
        self.gateSize = (120,120)
        self.gateTextSize = 20
        self.dragging = False

        self.addButton("ADD INPUT", (50,650), ButtonType.ADD_INPUT)
        self.addButton("ADD OUTPUT", (self.windowWidth - self.portMargin*2, 650), ButtonType.ADD_OUTPUT)
        self.addButton("ADD AND GATE", ((self.windowWidth-self.gateSize[0])/2, 650), ButtonType.ADD_AND_GATE)

    def run(self):
        while self.running:
            self.drawScreen()
            self.eventLoop()

    def drawScreen(self):
        self.screen.fill(self.backgroundColor)

        self.drawUI()
        self.drawObjects()
        self.changeColorOnHover()
        self.resetColor()

        pygame.display.flip()
        self.clock.tick(self.frameRate)

    def drawUI(self):
        y = self.windowHeight - self.menuHeight
        startPos = (0, y)
        endPos = (self.windowWidth, y)
        pygame.draw.aaline(self.screen, self.buttonTextColor, startPos, endPos)

    def drawObjects(self):
        for idx in self.objects.keys():
            self.objects[idx].draw(self.screen)

    def addButton(self, text: str, buttonPos: Tuple[int, int], buttonType: ButtonType):
        btnId = f"btn{self.buttonCounter}"
        newButtonView = ButtonView(buttonPos, self.buttonSize, btnId, text, buttonType, self.buttonColor, self.buttonTextColor, self.buttonTextSize)
        self.objects[newButtonView.id] = newButtonView
        self.buttonCounter += 1

    def addPort(self, idAndType, gateId=None):
        portId, portType = idAndType
        pos = (0,0) 
        portView = PortView(pos, self.portSize, portId, self.portColor, portType)
        self.objects[portView.id] = portView

        if gateId is not None:
            self.objects[gateId].objects[portView.id] = portView

    def addGate(self, payload):
        gateId, gateType, numInputs, numOutputs = payload 
        left = self.windowWidth / 2 - (self.gateSize[0]/2)
        top = ((self.windowHeight - self.menuHeight) / 2) - (self.gateSize[1]/2) 
        pos = (left, top)
        gateView = GateView(pos, self.gateSize, gateType, gateId, numInputs, numOutputs, self.buttonColor, self.buttonTextColor, self.screen, self.portColor, self.gateTextSize)
        self.objects[gateView.id] = gateView
    
        return gateView

    def centerCircuitPorts(self):
        workableHeight = self.windowHeight - self.menuHeight
        numInputs = self.count(PortType.CIRCUIT_INPUT)
        numOutputs = self.count(PortType.CIRCUIT_OUTPUT)
        slopeIn = workableHeight / (numInputs+1)
        slopeOut = workableHeight / (numOutputs+1)
        xIn = self.portMargin
        xOut = self.windowWidth - self.portMargin 
        counterIn = 1
        counterOut = 1
        for idx in self.objects.keys():
            obj = self.objects[idx]
            if obj.type == PortType.CIRCUIT_INPUT:
                x = xIn
                y = slopeIn * counterIn
                obj.pos = x,y 
                obj.x = x
                obj.y = y
                counterIn+=1
            elif obj.type == PortType.CIRCUIT_OUTPUT:
                x = xOut
                y = slopeOut * counterOut
                obj.pos = x,y 
                obj.x = x
                obj.y = y
                counterOut+=1

    def count(self, objectType):
        counter = 0
        for idx in self.objects.keys():
            obj = self.objects[idx]
            if obj.type == objectType:
                counter += 1
        return counter

    def linkPorts(self, payload):
        port1Id, port2Id = payload

    def changeColorOnHover(self):
        ho = self.getHoveredObject() 
        if ho is None:
            return
        ho.color = pygame.Color(255, 255, 255)

    def resetColor(self):
        ho = self.getHoveredObject()
        if ho is not None:
            return
        for idx in self.objects.keys():
            obj = self.objects[idx]
            if type(obj) is ButtonView or type(obj) is GateView:
                obj.color = self.buttonColor
            else:
                obj.color = self.portColor

    def getHoveredObject(self):
        mousePos = pygame.mouse.get_pos()
        for idx in self.objects.keys():
            obj = self.objects[idx]
            if obj.rect is None:
                continue
            if obj.rect.collidepoint(mousePos):
                return obj
        return None

    def getHoveredPort(self):
        obj = self.getHoveredObject()
        if type(obj) is PortView:
            return obj
        return None

    def getAreaMap(self):
        pass

    def checkForPortLinkAction(self):
        ho1 = self.getHoveredPort()

        if ho1 is None:
            return

        notValid = True
        while notValid:
            ho2 = self.getHoveredPort()
            print(f"ho1: {ho1}, ho2: {ho2}")
            if (ho2 is None) or (ho1 == ho2):
                continue
            if pygame.mouse.get_pressed()[0]:
                notValid = False

        return (ho1, ho2)

    def dragGate(self, event, obj):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        
        if self.dragging and type(obj) is GateView:
            mousePos = pygame.mouse.get_pos()
            pos = ((mousePos[0]-obj.width/2),(mousePos[1]-obj.height/2))
            obj.updatePos(self.screen, pos)
            
    def eventLoop(self):
        for event in pygame.event.get():
            hoveredObject = self.getHoveredObject()
            clicked = pygame.mouse.get_pressed()[0]

            if not clicked or hoveredObject is None:
                return

            if hoveredObject.type == ButtonType.ADD_INPUT:
                self.eventBus.publish(Event(EventType.CIRCUIT_INPUT))

            elif hoveredObject.type == ButtonType.ADD_OUTPUT:
                self.eventBus.publish(Event(EventType.CIRCUIT_OUTPUT))

            elif hoveredObject.type == ButtonType.ADD_AND_GATE:
                self.eventBus.publish(Event(EventType.GATE, GateType.AND_GATE))

            self.checkForPortLinkAction()
            self.dragGate(event, hoveredObject)
            

