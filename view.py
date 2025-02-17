import pygame
from typing import Tuple
from datetime import datetime
from event_bus import EventBus
from events import Event, EventType


class View:
    def __init__(self, eventBus: EventBus, windowWidth: int, windowHeight: int):
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
        self.inputColor = pygame.Color(50, 50, 50)

        self.eventBus = eventBus

    def update(self):
        self.screen.fill(self.backgroundColor)

        self.clearButtons()
        self.createButton("add input", (50,650))
        self.drawButtons()

        pygame.display.flip()
        self.clock.tick(self.frameRate)

    def run(self):
        while self.running:
            self.handleEvents()
            self.update()

    def createButton(self, text: str, buttonPos: Tuple[int, int]):
        font = pygame.font.SysFont("Source Code Pro", 10)
        renderedText = font.render(text, True, self.buttonTextColor)
        buttonSize = (80, 50)
        button = pygame.Rect(buttonPos, buttonSize)
        textPos = (buttonPos[0] + 15, buttonPos[1] + 20)
        self.buttons[self.buttonCounter] = {
            "rect": button,
            "renderedText": renderedText,
            "textPos": textPos,
            "text": text
        }
        self.buttonCounter += 1

    def drawButtons(self):
        for btn in self.buttons.values():
            pygame.draw.rect(self.screen, self.buttonColor, btn["rect"])
            self.screen.blit(btn["renderedText"], btn["textPos"])

    def clearButtons(self):
        self.buttons.clear()
        self.buttonCounter = 0

    def getHoveredButtonText(self):
        mousePos = pygame.mouse.get_pos()
        for btn in self.buttons.values():
            if btn["rect"].collidepoint(mousePos):
                return btn["text"]
        return None

    def drawInput(self):
        pos: Tuple[int, int] = (0,0)
        numInputs = len(self.inputs) + 1 
        x: int = 50
        y: int = 20 + self.windowHeight / numInputs 
        size: int = 10
        pygame.draw.circle(self.screen, self.inputColor, (x, y), size)
        self.update()

    def handleEvents(self):
        for event in pygame.event.get():
            hoveredText = self.getHoveredButtonText()
            clicked = pygame.mouse.get_pressed()[0]

            if hoveredText is not None and clicked:
                self.eventBus.publish(Event(EventType.ADD_INPUT_INCOMPLETE))

