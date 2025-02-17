import pygame
from typing import Tuple
from datetime import datetime
from events import Event, EventType
from event_bus import EventBus


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

        self.buttons = {}
        self.inputs = {}
        self.outputs = {}

        self.buttonTextColor = pygame.Color(200, 200, 200)
        self.backgroundColor = pygame.Color(40,28,52)
        self.buttonColor = pygame.Color(50, 50, 50)
        self.menuHeight = 100

        self.buttonCounter = 0
        self.inputCounter = 0

        self.createButton("ADD INPUT", (50,650))

    def drawScreen(self):
        self.screen.fill(self.backgroundColor)

        self.drawButtons()
        self.drawInputs()
        self.drawMenuBorder(self.windowHeight-self.menuHeight)

        pygame.display.flip()
        self.clock.tick(self.frameRate)

    def run(self):
        while self.running:
            self.drawScreen()
            self.eventLoop()

    def createButton(self, text: str, buttonPos: Tuple[int, int]):
        font: pygame.font = pygame.font.SysFont("Source Code Pro", 10) 
        renderedText = font.render(text, True, self.buttonTextColor)
        buttonSize: Tuple[int, int] = (80, 50)
        button = pygame.Rect(buttonPos, buttonSize)
        textPos: Tuple[int, int] = (buttonPos[0]+15,buttonPos[1]+20)
        self.buttons[self.buttonCounter] = {
            "rect": button,
            "renderedText": renderedText,
            "text": text, 
            "textPos": textPos
        }

    def drawButtons(self):
        for idx in range(0, self.buttonCounter+1):
            button = self.buttons[idx]["rect"]
            renderedText = self.buttons[idx]["renderedText"]
            textPos = self.buttons[idx]["textPos"]

            pygame.draw.rect(self.screen, self.buttonColor, button)
            self.screen.blit(renderedText, textPos)
        
    def clearButtons(self):
        self.buttons = {}

    def drawMenuBorder(self, y: int):
        startPos = (0, y)
        endPos = (self.windowWidth, y)
        pygame.draw.aaline(self.screen, self.buttonTextColor, startPos, endPos)

    def getHoveredButtonText(self):
        mousePos = pygame.mouse.get_pos()
        for idx in range(0, self.buttonCounter+1):
            btn = self.buttons[idx]
            if btn["rect"].collidepoint(mousePos):
                return btn["text"]

        return None

    def addInput(self, state: int):
        self.inputs[self.inputCounter] = {
            "state": state
        }
        self.inputCounter += 1

    def drawInputs(self):
        for idx, inp in enumerate(self.inputs):
            workableHeight = self.windowHeight - self.menuHeight
            x: Tuple[int, int] = 50
            y: Tuple[int, int] = (idx+1) * (workableHeight / (self.inputCounter+1))
            size: int = 10
            pygame.draw.circle(self.screen, self.buttonColor, (x,y), size)

    def eventLoop(self):
        for event in pygame.event.get():
            hoveredText = self.getHoveredButtonText()
            clicked = pygame.mouse.get_pressed()[0]

            if hoveredText is not None and clicked:
                self.eventBus.publish(Event(EventType.ADD_INPUT_INCOMPLETE))


