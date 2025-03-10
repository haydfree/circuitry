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
        if event.type == EventType.CIRCUIT_INPUT:
            idAndType = self.model.addPort(PortType.CIRCUIT_INPUT)
            self.view.addPort(idAndType)
            self.view.centerCircuitPorts()
            self.view.updateWires()

        elif event.type == EventType.CIRCUIT_OUTPUT:
            idAndType = self.model.addPort(PortType.CIRCUIT_OUTPUT)
            self.view.addPort(idAndType)
            self.view.centerCircuitPorts()
            self.view.updateWires()

        elif event.type == EventType.GATE:
            gateType = event.payload
            gateId, numInputs, numOutputs = self.model.addGate(gateType)
            portIds = self.model.addGatePorts(gateId)
            payload = gateId, gateType, numInputs, numOutputs
            gateView = self.view.addGate(payload)
            self.view.addGatePorts(gateId, portIds)

        elif event.type == EventType.LINK:
            portIds = event.payload
            self.model.linkPorts(portIds)
            self.view.linkPorts(portIds)
            self.view.addWire(portIds)

        elif event.type == EventType.UNLINK:
            wireId = event.payload
            inputId = self.view.objects[wireId].input.id 
            outputId = self.view.objects[wireId].output.id 
            self.model.unlinkPorts((inputId,outputId))
            self.view.unlinkPorts((inputId,outputId))
            self.view.removeWire((inputId,outputId))

        elif event.type == EventType.STATE_CHANGE:
            portId = event.payload
            self.model.stateChange(portId)
            self.view.stateChange(portId)
        
        elif event.type == EventType.STATE_VERIFY:
            stateMap = self.model.stateVerify()
            self.view.stateVerify(stateMap)
            self.model.runGates()

        elif event.type == EventType.CLEAR:
            self.model.clear()
            self.view.clear()

        elif event.type == EventType.SAVE:
            pass

        elif event.type == EventType.LOAD:
            pass



