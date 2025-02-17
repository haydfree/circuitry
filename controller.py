import pygame
from model import Model
from view import View
from event_bus import EventBus
from events import Event, EventType
from node import NodeType

class Controller():
    def __init__(self, eventBus: EventBus, model: Model, view: View):
        self.model = model
        self.view = view
        self.eventBus = eventBus

        self.eventBus.subscribe(self)
    
    def handleEvent(self, event: Event):
        if event.type == EventType.ADD_INPUT_INCOMPLETE:
            self.model.addNode(NodeType.INPUT)
        
        if event.type == EventType.ADD_INPUT_COMPLETE:
            self.view.addNode(NodeType.INPUT, event.payload.state)

        if event.type == EventType.ADD_OUTPUT_INCOMPLETE:
            self.model.addNode(NodeType.OUTPUT)

        if event.type == EventType.ADD_OUTPUT_COMPLETE:
            self.view.addNode(NodeType.OUTPUT, event.payload.state)


