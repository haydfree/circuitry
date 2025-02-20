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

    def handleEvent(self, event: Event):
        # purpose of controller: control the FLOW of the logic
        # being more explicit here and reducing coupling between functions would make it so much clearer and easier to debug
        if event.type == EventType.CIRCUIT_INPUT:
            inputStateAndId = self.model.addInput()
            self.view.addInput(inputStateAndId)
            self.view.centerInputPositions()

        elif event.type == EventType.CIRCUIT_OUTPUT:
            outputStateAndId = self.model.addOutput()
            self.view.addOutput(outputStateAndId)
            self.view.centerOutputPositions()

        elif event.type == EventType.GATE:
            gateType = event.payload
            gateId, _, numInputs, numOutputs = self.model.addGate(gateType)
            inputIds, outputIds = self.model.addGateNodes(gateId)
            payload = gateId, gateType, numInputs, numOutputs
            gateView = self.view.addGate(payload)
            gateView.addInputs(inputIds)
            gateView.addOutputs(outputIds)

        elif event.type == EventType.LINK:
            self.model.linkNodes()
            self.view.linkNodes()




