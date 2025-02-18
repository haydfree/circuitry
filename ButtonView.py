import pygame

class ButtonView:
    def __init__(self, pos, size, buttonId, text, buttonType, color, textColor):
        self.pos = pos
        self.size = size
        self.text = text
        self.type = buttonType
        self.color = color
        self.textColor = textColor
        self.id = buttonId

        self.font = pygame.font.SysFont("Source Code Pro", 10) 
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


