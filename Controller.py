import pygame
from Model import Model
from View import View
from Event import EventType, Event, EventBus
from Gate import GateType
from Port import PortType


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
            idAndType = self.model.addPort(PortType.CIRCUIT_INPUT)
            self.view.addPort(idAndType)
            self.view.centerCircuitPorts()

        elif event.type == EventType.CIRCUIT_OUTPUT:
            idAndType = self.model.addPort(PortType.CIRCUIT_OUTPUT)
            self.view.addPort(idAndType)
            self.view.centerCircuitPorts()

        elif event.type == EventType.GATE:
            gateType = event.payload
            gateId, _, numInputs, numOutputs = self.model.addGate(gateType)
            payload = gateId, gateType, numInputs, numOutputs
            gateView = self.view.addGate(payload)

            for idx in range(numInputs):
                idAndType = self.model.addPort(PortType.GATE_INPUT, gateId)
                self.view.addPort(idAndType, gateId)
            for idx in range(numOutputs):
                idAndType = self.model.addPort(PortType.GATE_OUTPUT, gateId)
                self.view.addPort(idAndType, gateId)
            gateView.centerGatePorts()

        elif event.type == EventType.LINK:
            self.model.linkNodes()
            self.view.linkNodes()




