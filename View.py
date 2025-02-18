import pygame
import pdb
from typing import Tuple
from Event import EventType, Event, EventBus
from InputView import InputView
from OutputView import OutputView
from ButtonView import ButtonView
from GateView import GateView
from ButtonType import ButtonType
from GateType import GateType
from NodeType import NodeType


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

        self.buttons = []
        self.inputs = []
        self.outputs = []
        self.gates = []
        self.buttonCounter = 0
        self.inputCounter = 0
        self.outputCounter = 0
        self.gateCounter = 0

        self.buttonTextColor = pygame.Color(200, 200, 200)
        self.backgroundColor = pygame.Color(40,28,52)
        self.buttonColor = pygame.Color(50, 50, 50)
        self.nodeColor = pygame.Color(20, 20, 20)
        self.buttonSize = (80,50)
        self.nodeSize = 10
        self.menuHeight = 100
        self.nodeMargin = 50
        self.gateSize = (80,80)
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

        self.drawMenuBorder(self.windowHeight-self.menuHeight)
        self.drawButtons()
        self.drawInputs()
        self.drawOutputs()
        self.drawGates()

        pygame.display.flip()
        self.clock.tick(self.frameRate)

    def drawMenuBorder(self, y: int):
        startPos = (0, y)
        endPos = (self.windowWidth, y)
        pygame.draw.aaline(self.screen, self.buttonTextColor, startPos, endPos)

    def drawButtons(self):
        for button in self.buttons:
            pygame.draw.rect(self.screen, self.buttonColor, button)
            self.screen.blit(button.renderedText, button.textPos)

    def drawInputs(self):
        for idx, inp in enumerate(self.inputs):
            rect = pygame.draw.circle(self.screen, self.nodeColor, inp.pos, self.nodeSize)
            inp.rect = rect

    def drawOutputs(self):
        for idx, out in enumerate(self.outputs):
            rect = pygame.draw.circle(self.screen, self.nodeColor, out.pos, self.nodeSize)
            out.rect = rect

    def drawGates(self):
        for gate in self.gates:
            pygame.draw.rect(self.screen, self.buttonColor, gate)
            self.screen.blit(gate.renderedText, gate.textPos)

    def addButton(self, text: str, buttonPos: Tuple[int, int], buttonType: ButtonType):
        newButtonView = ButtonView(buttonPos, self.buttonSize, self.buttonCounter, text, buttonType, self.buttonColor, self.buttonTextColor)
        self.buttons.append(newButtonView)
        self.buttonCounter += 1

    def addInput(self, state: int):
        workableHeight = self.windowHeight - self.menuHeight
        x = self.nodeMargin
        yOffset = workableHeight / (self.inputCounter + 2)
        for inp in self.inputs:
            inp.pos = (x,yOffset * (inp.id+1))
        y = yOffset * (self.inputCounter + 1)
        pos = (x,y)
        newInputView = InputView(pos, self.nodeSize, self.inputCounter, state)
        self.inputs.append(newInputView)
        self.inputCounter += 1

    def addOutput(self, state: int):
        workableHeight = self.windowHeight - self.menuHeight
        x = self.windowWidth - self.nodeMargin
        yOffset = workableHeight / (self.outputCounter + 2)
        for out in self.outputs:
            out.pos = (x,yOffset * (out.id+1))
        y = yOffset * (self.outputCounter + 1)
        pos = (x,y)
        newOutputView = OutputView(pos, self.nodeSize, self.outputCounter, state)
        self.outputs.append(newOutputView)
        self.outputCounter += 1

    def addGate(self, gateType: GateType, payload):
        text, numInputs, numOutputs = payload 
        pos = (self.windowWidth/2, self.windowHeight/2)
        newGateView = GateView(pos, self.gateSize, text, gateType, self.gateCounter, numInputs, numOutputs, self.buttonColor, self.buttonTextColor)
        self.gates.append(newGateView)
        self.gateCounter += 1

    def getHoveredObject(self):
        mousePos = pygame.mouse.get_pos()
        for btn in self.buttons:
            if btn.rect.collidepoint(mousePos):
                return btn
        for inp in self.inputs:
            if inp.rect.collidepoint(mousePos):
                return inp
        for out in self.outputs:
            if out.rect.collidepoint(mousePos):
                return out
        for gate in self.gates:
            if gate.rect.collidepoint(mousePos):
                return gate
        return None

    def eventLoop(self):
        for event in pygame.event.get():

            hoveredObject = self.getHoveredObject()
            clicked = pygame.mouse.get_pressed()[0]

            if hoveredObject is not None:

                if clicked and hoveredObject.type == ButtonType.ADD_INPUT:
                    self.eventBus.publish(Event(EventType.ADD_INPUT_MODEL))

                if clicked and hoveredObject.type == ButtonType.ADD_OUTPUT:
                    self.eventBus.publish(Event(EventType.ADD_OUTPUT_MODEL))

                if clicked and hoveredObject.type == ButtonType.ADD_AND_GATE:
                    self.eventBus.publish(Event(EventType.ADD_AND_GATE_MODEL))

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.dragging = True

                if event.type == pygame.MOUSEBUTTONUP:
                    self.dragging = False
                
                if event.type == pygame.MOUSEMOTION and self.dragging:
                    mousePos = pygame.mouse.get_pos()
                    gate = self.gates[hoveredObject.id]
                    pos = ((mousePos[0]-gate.width/2),(mousePos[1]-gate.height/2))
                    gate.updatePos(pos)
            

