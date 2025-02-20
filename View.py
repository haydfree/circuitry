import pygame
import pdb
import time
from datetime import datetime
from typing import Tuple
from Event import EventType, Event, EventBus
from InputView import InputView
from OutputView import OutputView
from ButtonView import ButtonView
from GateView import GateView
from ButtonType import ButtonType
from GateType import GateType
from NodeType import NodeType
from WireView import WireView
from InputType import InputType
from OutputType import OutputType


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
        self.uiComponents = {}

        self.buttonCounter = 0
        self.inputCounter = 0
        self.outputCounter = 0
        self.gateCounter = 0
        self.wireCounter = 0

        self.buttonTextColor = pygame.Color(200, 200, 200)
        self.backgroundColor = pygame.Color(40,28,52)
        self.buttonColor = pygame.Color(50, 50, 50)
        self.nodeColor = pygame.Color(20, 20, 20)
        self.buttonSize = (80, 50)
        self.buttonTextSize = 10
        self.nodeSize = 10
        self.menuHeight = 100
        self.nodeMargin = 50
        self.gateSize = (120,120)
        self.gateTextSize = 20
        self.dragging = False

        self.addButton("ADD INPUT", (50,650), ButtonType.ADD_INPUT)
        self.addButton("ADD OUTPUT", (self.windowWidth - self.nodeMargin*2, 650), ButtonType.ADD_OUTPUT)
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

    def addInput(self, inputIdAndState):
        state, inputId = inputIdAndState 
        pos = (0,0) 
        newInputView = InputView(pos, self.nodeSize, inputId, state, self.nodeColor)
        self.objects[newInputView.id] = newInputView
        self.inputCounter += 1

    def addOutput(self, outputIdAndState):
        state, outputId = outputIdAndState
        pos = (0,0)
        newOutputView = OutputView(pos, self.nodeSize, outputId, state, self.nodeColor)
        self.objects[newOutputView.id] = newOutputView
        self.outputCounter += 1

    def addGate(self, payload):
        gateId, gateType, numInputs, numOutputs = payload 
        left = self.windowWidth / 2 - (self.gateSize[0]/2)
        top = ((self.windowHeight - self.menuHeight) / 2) - (self.gateSize[1]/2) 
        pos = (left, top)
        newGateView = GateView(pos, self.gateSize, gateType, gateId, numInputs, numOutputs, self.buttonColor, self.buttonTextColor, self.screen, self.nodeColor, self.gateTextSize)
        self.objects[newGateView.id] = newGateView
        self.gateCounter += 1

    def centerInputPositions(self):
        workableHeight = self.windowHeight - self.menuHeight
        yOffset = workableHeight / (self.inputCounter + 1)
        x = self.nodeMargin
        for idx in self.objects.keys():
            obj = self.objects[idx]
            if type(obj) is InputView:
                obj.pos = x, yOffset * (idx+1)

    def centerOutputPositions(self):
        workableHeight = self.windowHeight - self.menuHeight
        yOffset = workableHeight / (self.outputCounter + 1)
        x = self.windowWidth - self.nodeMargin
        for idx in self.objects.keys():
            obj = self.objects[idx]
            if type(obj) is OutputView:
                obj.pos = x, yOffset * (idx+1)

    def linkNodes(self, payload):
        node1Id, node2Id = payload

    def changeColorOnHover(self):
        ho = self.getHoveredObject() 
        if ho is None:
            return
        ho.color = pygame.Color(255, 255, 255)

    def resetColor(self):
        ho = self.getHoveredObject()
        for idx in self.objects.keys():
            obj = self.objects[idx]
            if type(obj) is ButtonView or type(obj) is GateView:
                obj.color = self.buttonColor
            else:
                obj.color = self.nodeColor

    def getHoveredObject(self):
        mousePos = pygame.mouse.get_pos()
        for idx in self.objects.keys():
            obj = self.objects[idx]
            if obj.rect is None:
                continue
            if obj.rect.collidepoint(mousePos):
                return obj
        return None

    def getHoveredNode(self):
        obj = self.getHoveredObject()
        if type(obj) is GateType:
            return obj
        return None

    def getAreaMap(self):
        pass

    def checkForNodeLinkAction(self):
        ho1 = self.getHoveredNode()

        if ho1 is None:
            return

        notValid = True
        while notValid:
            ho2 = self.getHoveredNode()
            ev2 = pygame.event.wait()
            if (ho2 is None) or (ho1 == ho2) or (ev2.type != pygame.MOUSEBUTTONDOWN):
                continue
            notValid = False

        return (ho1, ho2)

    def dragGate(self, event, obj):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.dragging = True
        else:
            self.dragging = False
        
        if event.type == pygame.MOUSEMOTION and self.dragging and type(obj) is GateType:
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

            self.checkForNodeLinkAction()
            self.dragGate(event, hoveredObject)
            

