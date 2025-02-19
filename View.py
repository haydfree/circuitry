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
        self.wires = []
        self.buttonCounter = 0
        self.inputCounter = 0
        self.outputCounter = 0
        self.gateCounter = 0
        self.wireCounter = 0
        self.nodeCounter = 0

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

        self.drawMenuBorder(self.windowHeight-self.menuHeight)
        self.drawButtons()
        self.drawInputs()
        self.drawOutputs()
        self.drawGates()
        self.changeColorOnHover()
        self.resetColor()

        pygame.display.flip()
        self.clock.tick(self.frameRate)

    def drawMenuBorder(self, y: int):
        startPos = (0, y)
        endPos = (self.windowWidth, y)
        pygame.draw.aaline(self.screen, self.buttonTextColor, startPos, endPos)

    def drawButtons(self):
        for button in self.buttons:
            pygame.draw.rect(self.screen, button.color, button)
            self.screen.blit(button.renderedText, button.textPos)

    def drawInputs(self):
        for idx, inp in enumerate(self.inputs):
            rect = pygame.draw.circle(self.screen, inp.color, inp.pos, inp.size)
            inp.rect = rect

    def drawOutputs(self):
        for idx, out in enumerate(self.outputs):
            rect = pygame.draw.circle(self.screen, out.color, out.pos, out.size)
            out.rect = rect

    def drawGates(self):
        for gate in self.gates:
            pygame.draw.rect(self.screen, gate.color, gate)
            self.screen.blit(gate.renderedText, gate.textPos)
            gate.drawInputs()
            gate.drawOutputs()

    def addButton(self, text: str, buttonPos: Tuple[int, int], buttonType: ButtonType):
        newButtonView = ButtonView(buttonPos, self.buttonSize, self.buttonCounter, text, buttonType, self.buttonColor, self.buttonTextColor, self.buttonTextSize)
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
        newInputView = InputView(pos, self.nodeSize, self.nodeCounter, state, self.nodeColor)
        self.inputs.append(newInputView)
        self.inputCounter += 1
        self.nodeCounter += 1

    def addOutput(self, state: int):
        workableHeight = self.windowHeight - self.menuHeight
        x = self.windowWidth - self.nodeMargin
        yOffset = workableHeight / (self.outputCounter + 2)
        for out in self.outputs:
            out.pos = (x,yOffset * (out.id+1))
        y = yOffset * (self.outputCounter + 1)
        pos = (x,y)
        newOutputView = OutputView(pos, self.nodeSize, self.nodeCounter, state, self.nodeColor)
        self.outputs.append(newOutputView)
        self.outputCounter += 1
        self.nodeCounter += 1

    def addGate(self, gateType: GateType, payload):
        text, numInputs, numOutputs = payload 
        left = self.windowWidth / 2 - (self.gateSize[0]/2)
        top = ((self.windowHeight - self.menuHeight) / 2) - (self.gateSize[1]/2) 
        pos = (left, top)
        newGateView = GateView(pos, self.gateSize, text, gateType, self.gateCounter, numInputs, numOutputs, self.buttonColor, self.buttonTextColor, self.screen, self.nodeColor, self.gateTextSize)
        self.gates.append(newGateView)
        newGateView.addInputs(self.nodeCounter)
        self.nodeCounter += numInputs
        newGateView.addOutputs(self.nodeCounter)
        self.nodeCounter += numOutputs
        self.gateCounter += 1

    def linkNodes(self, node1Id, node2Id):
        pass

    def changeColorOnHover(self):
        ho = self.getHoveredObject() 
        if ho is None:
            return
        ho.color = pygame.Color(255, 255, 255)

    def resetColor(self):
        ho = self.getHoveredObject()
        for btn in self.buttons:
            if ho != btn:
                btn.color = self.buttonColor
        for inp in self.inputs:
            if ho != inp:
                inp.color = self.nodeColor
        for out in self.outputs:
            if ho != out:
                out.color = self.nodeColor
        for gate in self.gates:
            if ho != gate:
                gate.color = self.buttonColor
            for inp in gate.inputs:
                if ho != inp:
                    inp.color = gate.nodeColor
            for out in gate.outputs:
                if ho != out:
                    out.color = gate.nodeColor

    def getHoveredObject(self):
        mousePos = pygame.mouse.get_pos()
        ho = None
        for btn in self.buttons:
            if btn.rect.collidepoint(mousePos):
                ho = btn 
        for inp in self.inputs:
            if inp.rect.collidepoint(mousePos):
                ho = inp
        for out in self.outputs:
            if out.rect.collidepoint(mousePos):
                ho = out
        for gate in self.gates:
            if gate.rect.collidepoint(mousePos):
                ho = gate
            for inp in gate.inputs:
                if inp.rect.collidepoint(mousePos):
                    ho = inp
            for out in gate.outputs:
                if out.rect.collidepoint(mousePos):
                    ho = out
        return ho

    def getAreaMap(self):
        obstacleCoords = []

        for inp in self.inputs:
            for x in range(inp.x, inp.x+inp.width+1):
                for y in range(inp.top, inp.top+inp.height+1):
                    obstacleCoords.append((x,y))
        for out in self.outputs:
            for x in range(out.x, out.x+out.width+1):
                for y in range(out.top, out.top+out.height+1):
                    obstacleCoords.append((x,y))
        for gate in self.gates:
            for x in range(gate.x, gate.x+gate.width+1):
                for y in range(gate.top, gate.top+gate.height+1):
                    obstacleCoords.append((x,y))
        for wire in self.wires:
            pass

    def eventLoop(self):
        for event in pygame.event.get():
            hoveredObject = self.getHoveredObject()
            clicked = pygame.mouse.get_pressed()[0]

            if clicked and hoveredObject is not None:
                if hoveredObject.type == ButtonType.ADD_INPUT:
                    self.eventBus.publish(Event(EventType.ADD_INPUT_MODEL, hoveredObject.id))

                if hoveredObject.type == ButtonType.ADD_OUTPUT:
                    self.eventBus.publish(Event(EventType.ADD_OUTPUT_MODEL, hoveredObject.id))

                if hoveredObject.type == ButtonType.ADD_NOT_GATE:
                    self.eventBus.publish(Event(EventType.ADD_NOT_GATE_MODEL))

                if hoveredObject.type == ButtonType.ADD_AND_GATE:
                    self.eventBus.publish(Event(EventType.ADD_AND_GATE_MODEL))

                if hoveredObject.type == ButtonType.ADD_NAND_GATE:
                    self.eventBus.publish(Event(EventType.ADD_NAND_GATE_MODEL))

                if hoveredObject.type == ButtonType.ADD_OR_GATE:
                    self.eventBus.publish(Event(EventType.ADD_OR_GATE_MODEL))

                if hoveredObject.type == ButtonType.ADD_XOR_GATE:
                    self.eventBus.publish(Event(EventType.ADD_XOR_GATE_MODEL))

                if hoveredObject.type == ButtonType.ADD_NOR_GATE:
                    self.eventBus.publish(Event(EventType.ADD_NOR_GATE_MODEL))

                if hoveredObject.type == ButtonType.ADD_XNOR_GATE:
                    self.eventBus.publish(Event(EventType.ADD_XNOR_GATE_MODEL))

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.dragging = True

                if event.type == pygame.MOUSEBUTTONUP:
                    self.dragging = False
                
                # drag gates around
                if event.type == pygame.MOUSEMOTION and self.dragging and hoveredObject in self.gates:
                    mousePos = pygame.mouse.get_pos()
                    gate = self.gates[hoveredObject.id]
                    pos = ((mousePos[0]-gate.width/2),(mousePos[1]-gate.height/2))
                    gate.updatePos(self.screen, pos)
                
                # link node to another node
                clickedNode = hoveredObject in self.inputs or hoveredObject in self.outputs
                for gate in self.gates:
                    if hoveredObject in gate.inputs or hoveredObject in gate.outputs:
                        clickedNode = True
                if clickedNode:
                    found = False
                    clickedAnotherNode = False
                    while not clickedAnotherNode:
                        ho2 = self.getHoveredObject()
                        clickedAnotherNode = (hoveredObject != ho2) and (hoveredObject is not None) and (ho2 is not None)
                        ev2 = pygame.event.wait()
                        if (ho2 is None) or \
                            (hoveredObject == ho2) or \
                            (hoveredObject is None) or \
                            (ev2.type != pygame.MOUSEBUTTONDOWN) or \
                            not (ho2.type == NodeType.INPUT or ho2.type == NodeType.OUTPUT):
                            clickedAnotherNode = False 
                            continue
                        
                        clickedAnotherNode = True
                    print(f"linked node1: {hoveredObject.type} {hoveredObject.id} and node2: {ho2.type} {ho2.id}")
                    self.eventBus.publish(Event(EventType.LINK_NODES_MODEL, (hoveredObject.id, ho2.id)))
                     

            

