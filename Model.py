from Port import Port, PortType
from Gate import Gate, GateType
from Event import EventType, Event, EventBus

class Model:
    def __init__(self, eventBus: EventBus):
        self.eventBus = eventBus

        self.objects = {}
        self.objectCounter = 0

    def addPort(self, portType, gateId=None):
        portId = self.objectCounter
        newPort = Port(portId, portType)
        self.objects[newPort.id] = newPort
        self.objectCounter += 1

        if gateId is not None:
            self.objects[gateId].objects[newPort.id] = newPort

        return newPort.id, newPort.type

    def addGate(self, gateType: GateType):
        gateId = self.objectCounter
        if gateType == GateType.NOT_GATE:
            numInputs = 1
        else:
            numInputs = 2
        numOutputs = 1
        newGate = Gate(gateId, gateType, numInputs, numOutputs)
        self.objects[newGate.id] = newGate
        self.objectCounter += 1

        return (newGate.id, newGate.type, newGate.numInputs, newGate.numOutputs)

    def addGatePorts(self, gateId):
        gate = self.objects[gateId] 
        inputIds = []
        outputIds = []
        for idx in range(gate.numInputs):
            _, newInputId = self.addInput()
            gate.objects[newInputId] = self.objects[newInputId]
            inputIds.append(newInputId)
        for idx in range(gate.numOutputs):
            _, newOutputId = self.addOutput()
            gate.objects[newOutputId] = self.objects[newOutputId]
            outputIds.append(newOutputId)

        return (inputIds, outputIds)

    def linkPorts(self, portIds):
        port1Id, port2Id = portIds
        port1 = self.objects[port1Id]
        port2 = self.objects[port2Id]
        port2.input = port1
        port1.output = port2


