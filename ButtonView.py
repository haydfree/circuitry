import pygame
from enum import Enum, auto


class ButtonType(Enum):
    ADD_INPUT = auto()
    ADD_OUTPUT = auto()
    ADD_NOT_GATE = auto()
    ADD_AND_GATE = auto()
    ADD_NAND_GATE = auto()
    ADD_OR_GATE = auto()
    ADD_XOR_GATE = auto()
    ADD_NOR_GATE = auto()
    ADD_XNOR_GATE = auto()

    CLEAR = auto()
    QUIT = auto()


class ButtonView:
    def __init__(self, pos, size, buttonId, text, buttonType, color, textColor, textSize):
        self.pos = pos
        self.size = size
        self.text = text
        self.textSize = textSize
        self.type = buttonType
        self.color = color
        self.textColor = textColor
        self.id = buttonId
        self.oldColor = color

        self.font = pygame.font.SysFont("Source Code Pro", self.textSize) 
        self.renderedText = self.font.render(text, True, self.textColor)
        self.left, self.top = pos
        self.width, self.height = self.size
        self.rect = pygame.Rect(self.pos, self.size)
        renderedTextWidth = self.renderedText.get_width()
        renderedTextHeight = self.renderedText.get_height()
        widthDiff = self.width - renderedTextWidth
        heightDiff = self.height - renderedTextHeight
        self.textPos = (self.left+widthDiff/2, self.top+heightDiff/2)
        self.buttonType = buttonType

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect) 
        screen.blit(self.renderedText, self.textPos)


