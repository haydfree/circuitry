import pygame
from Model import Model
from View import View
from Event import EventType, Event, EventBus
from GateType import GateType
from NodeType import NodeType
from InputType import InputType
from OutputType import OutputType


class Controller():
    def __init__(self, eventBus: EventBus, model: Model, view: View):
        self.model = model
        self.view = view
        self.eventBus = eventBus
        self.eventBus.subscribe(self)

    def findByIdModel(self, objectId):
        return self.model.findById(objectId) 

    def findByIdView(self, objectId):
        return self.view.findById(objectId)
    
    def handleEvent(self, event: Event):
        if event.type == EventType.ADD_INPUT_MODEL:
            self.model.addInput(InputType.CIRCUIT_INPUT)
        
        elif event.type == EventType.ADD_INPUT_VIEW:
            self.view.addInput(event.payload)
        
        elif event.type == EventType.ADD_GATE_INPUT_VIEW:
            gateId, inputId = event.payload
            self.findByIdView(gateId).addInputs(inputId)

        elif event.type == EventType.ADD_OUTPUT_MODEL:
            self.model.addOutput(OutputType.CIRCUIT_OUTPUT)

        elif event.type == EventType.ADD_OUTPUT_VIEW:
            self.view.addOutput(event.payload)

        elif event.type == EventType.ADD_GATE_INPUT:
            self.model.addInput(event.payload)

        elif event.type == EventType.ADD_GATE_OUTPUT:
            self.model.addOutput(event.payload)

        elif event.type == EventType.ADD_GATE_OUTPUT_VIEW:
            gateId, outputId = event.payload
            self.findByIdView(gateId).addOutputs(outputId)

        elif event.type == EventType.ADD_AND_GATE_MODEL:
            self.model.addGate(GateType.AND_GATE)

        elif event.type == EventType.ADD_AND_GATE_VIEW:
            self.view.addGate(event.payload)

        elif event.type == EventType.LINK_NODES_MODEL:
            self.model.linkNodes(event.payload)

        elif event.type == EventType.LINK_NODES_VIEW:
            self.view.linkNodes(event.payload) 


