import pygame
from model import Model
from view import View
from event_bus import EventBus
from events import Event, EventType

class Controller():
    def __init__(self, eventBus: EventBus, model: Model, view: View):
        self.model = model
        self.view = view
        self.eventBus = eventBus

        self.eventBus.subscribe(self)
    
    def handleEvent(self, event: Event):
        if event.type == EventType.ADD_INPUT_INCOMPLETE:
            self.model.addInput()
        
        if event.type == EventType.ADD_INPUT_COMPLETE:
            self.view.addInput(event.payload.state)

        if event.type == EventType.ADD_OUTPUT_INCOMPLETE:
            self.model.addOutput()

        if event.type == EventType.ADD_OUTPUT_COMPLETE:
            self.view.addOutput(event.payload.state)


