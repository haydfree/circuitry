import pygame



class PortView:
    def __init__(self, pos, size, portId, color, portType):
        self.pos = pos
        self.size = size
        self.x, self.y = pos
        self.id = portId
        self.color = color
        self.type = portType
        self.mainColor = color
        self.hoverColor = (255,255,255)
        self.stateColor = (0,255,0)

        self.state = None 
        self.rect = None
        self.input = None
        self.output = None
        self.wire = None

    def draw(self, screen):
        self.rect = pygame.draw.circle(screen, self.color, self.pos, self.size)



