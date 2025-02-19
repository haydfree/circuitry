import pygame
from Model import Model
from View import View
from Event import EventType, Event, EventBus
from GateType import GateType
from NodeType import NodeType


class Controller():
    def __init__(self, eventBus: EventBus, model: Model, view: View):
        self.model = model
        self.view = view
        self.eventBus = eventBus

        self.eventBus.subscribe(self)
    
    def handleEvent(self, event: Event):
        if event.type == EventType.ADD_INPUT_MODEL:
            self.model.addInput(event.payload)
        
        if event.type == EventType.ADD_INPUT_VIEW:
            self.view.addInput(event.payload.state)

        if event.type == EventType.ADD_OUTPUT_MODEL:
            self.model.addOutput(event.payload)

        if event.type == EventType.ADD_OUTPUT_VIEW:
            self.view.addOutput(event.payload.state)

        if event.type == EventType.ADD_AND_GATE_MODEL:
            self.model.addGate(GateType.AND_GATE)

        if event.type == EventType.ADD_AND_GATE_VIEW:
            self.view.addGate(GateType.AND_GATE, event.payload)

        if event.type == EventType.LINK_NODES_MODEL:
            self.model.linkNodes(event.payload[0], event.payload[1])

        if event.type == EventType.LINK_NODES_VIEW:
            self.view.linkNodes(event.payload[0], event.payload[1]) 


