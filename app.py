import pygame
from model import Model
from view import View
from controller import Controller
from event_bus import EventBus


class App:
    def __init__(self):
        self.eventBus = EventBus()
        self.model = Model(self.eventBus)
        self.view = View(self.eventBus, 1280, 720)
        self.controller = Controller(self.eventBus, self.model, self.view)

    def run(self):
        self.view.run()



if __name__ == "__main__":
    app = App()
    app.run()
        

