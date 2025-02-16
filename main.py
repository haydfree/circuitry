import pygame
import pygame.gfxdraw
from pygame.locals import *
import random

pygame.init()
screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
running = True

paths = []
wires = []

class Wire:
    def __init__(self, path):
        self.path = path

class Gate:
    def __init__(self, inputs=[], outputs=[]):
        self.inputs = inputs
        self.outputs = outputs

class Input:
    def __init__(self):
        pass

class Output:
    def __init__(self):
        pass

        

def getPath():
    if not mouseDown:
        return
    x, y = pygame.mouse.get_pos()
    paths.append((x,y))

def smoothPath(color, granularity):
    lenPaths = len(paths)
    if lenPaths < 2:
        return
    for i in range(0, lenPaths-1):
        x1,y1 = paths[i+1]
        x0,y0 = paths[i]
        xDiff,yDiff = x1-x0,y1-y0
        for idx in range(0, granularity):
            xn,yn = x0+idx*(xDiff/granularity),y0+idx*(yDiff/granularity)
            pygame.draw.circle(screen, color, (xn,yn), 4)

def draw(mouseX, mouseY, color):
    pygame.draw.circle(screen, color, (mouseX, mouseY), 4)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
    
    mouseDown = pygame.mouse.get_pressed()[0]
    if mouseDown:
        color = pygame.Color(0,0,255)
        mouseX, mouseY = pygame.mouse.get_pos()
        getPath()
        smoothPath(color, 100)

    if not mouseDown:
        if paths:
            wires.append(Wire(paths))
        paths = []

    if wires:
        print(wires)

    escKeyPressed = pygame.key.get_pressed()[K_ESCAPE] == True
    if escKeyPressed:
        running = False
        pygame.display.quit()
        pygame.quit()
            
    pygame.display.flip()
    clock.tick(30)


pygame.quit()
