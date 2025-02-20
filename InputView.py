import pygame
from NodeType import NodeType



class InputView:
    def __init__(self, pos, size, inputId, state, color):
        self.pos = pos
        self.size = size
        self.x, self.y = pos
        self.id = inputId
        self.state = state 
        self.rect = None
        self.type = NodeType.INPUT
        self.color = color

        self.input = None
        self.output = None

    def draw(self, screen):
        self.rect = pygame.draw.circle(screen, self.color, self.pos, self.size)



