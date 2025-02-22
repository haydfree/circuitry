import pygame
import pdb
import time
import sys
from typing import Tuple
from Port import PortType
from Gate import GateType
from Event import EventType, Event, EventBus
from ButtonView import ButtonView, ButtonType
from GateView import GateView
from PortView import PortView
from WireView import WireView


class View:
    def __init__(self, eventBus: EventBus, windowWidth: int, windowHeight: int):
        self.eventBus = eventBus

        pygame.init()
        self.screen: pygame.display = pygame.display.set_mode((windowWidth, windowHeight))
        self.clock: pygame.time.Clock = pygame.time.Clock()
        pygame.display.set_caption("Circuitry")
        self.running: bool = True
        self.frameRate = 60
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        self.hoveredObject = None

        self.objects = {}
        self.buttonCounter = 0
        self.wireCounter = 0

        self.buttonTextColor = pygame.Color(200, 200, 200)
        self.backgroundColor = pygame.Color(40,28,52)
        self.buttonColor = pygame.Color(50, 50, 50)
        self.portColor = pygame.Color(255,0,0)
        self.buttonSize = (80, 50)
        self.buttonTextSize = 20
        self.portSize = 10
        self.menuHeight = 100
        self.portMargin = 50
        self.gateSize = (120,120)
        self.gateTextSize = 20
        self.dragging = False
        self.wireColor = (0,0,0)

        self.addAllButtons()
 
    def run(self):
        while self.running:
            self.eventLoop()
            self.drawScreen()

    def drawScreen(self):
        self.screen.fill(self.backgroundColor)

        self.drawUI()
        self.drawObjects()
        self.changeColorOnHover()
        self.resetColor()
        self.changeColorWithState()

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

    def clear(self):
        self.objects = {}
        self.buttonCounter = 0
        self.wireCounter = 0
        self.addAllButtons()

    def quit(self):
        self.clear()
        pygame.display.quit()
        pygame.quit()
        sys.exit()

    def addAllButtons(self):
        map1 = {"CLEAR": ButtonType.CLEAR, "QUIT": ButtonType.QUIT}
        map2 = {
            "INPUT": ButtonType.ADD_INPUT,
            "OUTPUT": ButtonType.ADD_OUTPUT,
            "NOT": ButtonType.ADD_NOT_GATE,
            "AND": ButtonType.ADD_AND_GATE,
            "NAND": ButtonType.ADD_NAND_GATE,
            "OR": ButtonType.ADD_OR_GATE,
            "NOR": ButtonType.ADD_NOR_GATE,
            "XOR": ButtonType.ADD_XOR_GATE,
            "XNOR": ButtonType.ADD_XNOR_GATE
        }
        x,y = 0,0
        pos = x,y
        for idx in map1.keys():
            btnType = map1[idx]
            self.addButton(idx, pos, btnType)
            x+=90
            pos=x,y

        x,y = 50,650
        pos = x,y
        for idx in map2.keys():
            btnType = map2[idx]
            self.addButton(idx, pos, btnType)
            x+=(self.windowWidth-50)/len(map2.keys())
            pos=x,y

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

    def addGatePorts(self, gateId, portIds):
        inputPortIds, outputPortIds = portIds
        gate = self.objects[gateId]
        for portId in inputPortIds:
            self.addPort((portId, PortType.GATE_INPUT), gateId)
        for portId in outputPortIds:
            self.addPort((portId, PortType.GATE_OUTPUT), gateId)

    def addWire(self, portIds):
        p1, p2 = self.objects[portIds[0]], self.objects[portIds[1]]
        wire = WireView(p1, p2, self.wireColor, self.objects)
        p1.wire = wire
        wireId = f"wire{self.wireCounter}"
        wire.pathfind()
        self.objects[wireId] = wire
        self.wireCounter += 1

    def updateWires(self):
        for idx in self.objects.keys():
            obj = self.objects[idx]
            if type(obj) is WireView:
                obj.rects = []
                obj.pathfind()

    def stateChange(self, portId):
        p = self.objects[portId]
        p.state = not p.state

    def stateVerify(self, stateMap):
        for idx in stateMap.keys():
            port = self.objects[idx]
            port.state = stateMap[port.id]
    
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

    def linkPorts(self, portIds):
        port1Id, port2Id = portIds
        port1 = self.objects[port1Id]
        port2 = self.objects[port2Id]
        port2.input = port1
        port2.state = port1.state
        port1.output = port2

    def changeColorWithState(self):
        for idx in self.objects.keys():
            obj = self.objects[idx]
            if type(obj) is PortView:
                if obj.state == 1:
                    obj.color = obj.stateColor

    def changeColorOnHover(self):
        currentHo = self.getHoveredObject()
        if currentHo is not None:
            currentHo.color = currentHo.hoverColor

    def resetColor(self):
        currentHo = self.getHoveredObject()
        for idx in self.objects.keys():
            obj = self.objects[idx]
            if currentHo == obj:
                continue
            obj.color = obj.mainColor

    def getHoveredObject(self):
        mousePos = pygame.mouse.get_pos()
        for idx in self.objects.keys():
            obj = self.objects[idx]
            if obj.rect is None:
                continue
            if obj.rect.collidepoint(mousePos):
                self.hoveredObject = obj
                return obj
        return None

    def getHoveredPort(self):
        obj = self.getHoveredObject()
        if type(obj) is PortView:
            return obj
        return None

    def checkForPortLinkAction(self):
        ho1 = self.getHoveredPort()

        if ho1 is None:
            return None

        notValid = True
        while notValid:
            pygame.event.wait()
            ho2 = self.getHoveredPort()
            if (ho2 is None) or (ho1 == ho2):
                continue
            if pygame.mouse.get_pressed()[0]:
                notValid = False

        return (ho1.id, ho2.id)

    def dragGate(self, event, obj):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        
        if self.dragging and type(obj) is GateView:
            mousePos = pygame.mouse.get_pos()
            pos = ((mousePos[0]-obj.width/2),(mousePos[1]-obj.height/2))
            obj.updatePos(self.screen, pos)
            self.updateWires()

    def eventLoop(self):
        self.eventBus.publish(Event(EventType.STATE_VERIFY))
        for event in pygame.event.get():
            hoveredObject = self.getHoveredObject()
            lmbClicked = pygame.mouse.get_pressed()[0]
            rmbClicked = pygame.mouse.get_pressed()[2]

            if hoveredObject is None:
                continue

            if rmbClicked and hoveredObject.type == PortType.CIRCUIT_INPUT:
                self.eventBus.publish(Event(EventType.STATE_CHANGE, hoveredObject.id))

            if not lmbClicked:
                continue 

            if hoveredObject.type == ButtonType.ADD_INPUT:
                self.eventBus.publish(Event(EventType.CIRCUIT_INPUT))
            elif hoveredObject.type == ButtonType.ADD_OUTPUT:
                self.eventBus.publish(Event(EventType.CIRCUIT_OUTPUT))
            elif hoveredObject.type == ButtonType.ADD_NOT_GATE:
                self.eventBus.publish(Event(EventType.GATE, GateType.NOT_GATE))
            elif hoveredObject.type == ButtonType.ADD_AND_GATE:
                self.eventBus.publish(Event(EventType.GATE, GateType.AND_GATE))
            elif hoveredObject.type == ButtonType.ADD_NAND_GATE:
                self.eventBus.publish(Event(EventType.GATE, GateType.NAND_GATE))
            elif hoveredObject.type == ButtonType.ADD_OR_GATE:
                self.eventBus.publish(Event(EventType.GATE, GateType.OR_GATE))
            elif hoveredObject.type == ButtonType.ADD_NOR_GATE:
                self.eventBus.publish(Event(EventType.GATE, GateType.NOR_GATE))
            elif hoveredObject.type == ButtonType.ADD_XOR_GATE:
                self.eventBus.publish(Event(EventType.GATE, GateType.XOR_GATE))
            elif hoveredObject.type == ButtonType.ADD_XNOR_GATE:
                self.eventBus.publish(Event(EventType.GATE, GateType.XNOR_GATE))
            elif hoveredObject.type == ButtonType.CLEAR:
                self.eventBus.publish(Event(EventType.CLEAR))
            elif hoveredObject.type == ButtonType.QUIT:
                self.quit()

            self.dragGate(event, hoveredObject)

            linkablePorts = self.checkForPortLinkAction()
            if linkablePorts is not None:
                self.eventBus.publish(Event(EventType.LINK, linkablePorts))

            

