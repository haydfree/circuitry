import pygame
from NodeType import NodeType


class OutputView:
    def __init__(self, pos, size, outputId, state, color):
        self.pos = pos
        self.size = size
        self.x, self.y = pos
        self.id = outputId
        self.state = state 
        self.rect = None
        self.type = NodeType.OUTPUT
        self.color = color

        self.input = None
        self.output = None

    def draw(self, screen):
        self.rect = pygame.draw.circle(screen, self.color, self.pos, self.size)


