from Input import Input
from Output import Output
from Gate import Gate
from Event import EventType, Event, EventBus
from GateType import GateType
from NodeType import NodeType
from InputType import InputType
from OutputType import OutputType

class Model:
    def __init__(self, eventBus: EventBus):
        self.eventBus = eventBus

        self.objects = {}
        self.objectCounter = 0

    def addInput(self):
        state = 0
        inputId = self.objectCounter
        newInput = Input(inputId, state, None, None)
        self.objects[newInput.id] = newInput
        self.objectCounter += 1

        return (newInput.state, newInput.id)

    def addOutput(self):
        state = 0
        outputId = self.objectCounter
        newOutput = Output(outputId, state, None, None)
        self.objects[newOutput.id] = newOutput
        self.objectCounter += 1

        return (newOutput.state, newOutput.id)

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
        for inp in range(gate.numInputs):
            newInput = self.addInput()
            self.objects[newInput.id] = newInput
            gate.objects[newInput.id] = newInput
        for out in range(gate.numOutputs):
            newOutput = self.addOutput()
            self.objects[newOutput.id] = newOutput
            gate.objects[newOutput.id] = newOutput

    def linkNodes(self, nodeIds):
        node1Id, node2Id = nodeIds
        node1 = self.objects[node1Id]
        node2 = self.objects[node2Id]
        node2.input = node1
        node1.output = node2


