from Port import Port, PortType
from Gate import Gate, GateType
from Event import EventType, Event, EventBus

class Model:
    def __init__(self, eventBus: EventBus):
        self.eventBus = eventBus

        self.objects = {}
        self.objectCounter = 0

    def addPort(self, portType):
        portId = self.objectCounter
        newPort = Port(portId, portType)
        self.objects[newPort.id] = newPort
        self.objectCounter += 1

        return newPort.id

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

    def addGateNodes(self, gateId):
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

    def linkNodes(self, nodeIds):
        node1Id, node2Id = nodeIds
        node1 = self.objects[node1Id]
        node2 = self.objects[node2Id]
        node2.input = node1
        node1.output = node2


