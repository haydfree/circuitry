from collections import deque
import pygame
import math


class WireView:
    def __init__(self, inputPort, outputPort, color, objects):
        self.input = inputPort
        self.output = outputPort
        self.objects = objects
        self.rect = None
        self.type = None
        self.color = color
        self.mainColor = color
        self.hoverColor = (255,255,255)

        self.lineWidth = 3
        self.rects = []


    def draw(self, screen):
        for line in self.rects:
            pygame.draw.rect(screen, self.color, line)

    def isObstacle(self, pos):
        for idx in self.objects.keys():
            obj = self.objects[idx]
            if obj.rect.collidepoint(pos):
                return True
        return False

    def getNeighbors(self, pos):
        x, y = pos
        up = (x, y-1)
        down = (x, y+1)
        left = (x-1, y)
        right = (x+1, y)

        return (up, down, left, right)

    def getMidpoints(self, startPos, endPos):
        startX, endX = startPos[0], endPos[0]
        startY, endY = startPos[1], endPos[1]

        diffX = int((endX - startX) / 2)
        diffY = int((endY - startY) / 2)

        midX = startX + diffX
        midY = startY + diffY

        return (midX, midY)

    def pathfind(self):
        startX, startY = self.input.pos
        startPos = startX, startY
        endX, endY = self.output.pos
        endPos = endX, endY
        midX, midY = self.getMidpoints(startPos, endPos)
        midPos = midX, midY

        if endY > startY:
            y2 = startY
        else:
            y2 = endY

        line1 = pygame.Rect(startX, startY, abs(midX-startX), self.lineWidth)
        line2 = pygame.Rect(midX, y2, self.lineWidth, abs(endY-startY))
        line3 = pygame.Rect(midX, endY, abs(endX-midX), self.lineWidth)

        self.rects.append(line1)
        self.rects.append(line2)
        self.rects.append(line3)



