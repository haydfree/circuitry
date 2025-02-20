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

        self.inputs = []
        self.outputs = [] 
        self.gates = []

        self.objectCounter = 0

    def findById(self, objectId):
        for inp in self.inputs:
            if inp.id == objectId:
                return inp
        for out in self.outputs:
            if out.id == objectId:
                return out
        for gate in self.gates:
            if gate.id == objectId:
                return gate
            for inp in gate.inputs:
                if inp.id == objectId:
                    return inp
            for out in gate.outputs:
                if out.id == objectId:
                    return out
        return None

    def addInput(self, inputType: InputType, gateId=None):
        state = 0
        inputId = self.objectCounter
        newInput = Input(inputId, state, None, None)
        print(f"inputId: {inputId}")
        
        self.objectCounter += 1
        self.inputs.append(newInput)
        viewPayload = (newInput.id, newInput.state)
        if inputType == InputType.CIRCUIT_INPUT:
            self.eventBus.publish(Event(EventType.ADD_INPUT_VIEW, viewPayload))

    def addOutput(self, outputType: OutputType, gateId=None):
        state = 0
        outputId = self.objectCounter
        print(f"outputId: {outputId}")
        newOutput = Output(outputId, state, None, None)

        self.objectCounter += 1
        self.outputs.append(newOutput)
        viewPayload = (newOutput.id, newOutput.state)
        if outputType == OutputType.CIRCUIT_OUTPUT:
            self.eventBus.publish(Event(EventType.ADD_OUTPUT_VIEW, viewPayload))

    def addGate(self, payload: GateType):
        gateId = self.objectCounter
        print(f"gateId: {gateId}")
        gateType = payload
        if payload == GateType.NOT_GATE:
            inputs = 1
            outputs = 1
            newGate = Gate(gateId, payload)
            self.gates.append(newGate)
            self.addGateNodes(newGate, inputs, outputs)
            viewPayload = (gateId, gateType, inputs, outputs)
            self.eventBus.publish(Event(EventType.ADD_NOT_GATE_VIEW, viewPayload))

        if payload == GateType.AND_GATE:
            inputs = 2
            outputs = 1
            newGate = Gate(gateId, payload)
            self.gates.append(newGate)
            self.addGateNodes(newGate, inputs, outputs)
            viewPayload = (gateId, gateType, inputs, outputs)
            self.eventBus.publish(Event(EventType.ADD_AND_GATE_VIEW, viewPayload))

        for idx in range(inputs):
            payload = (gateId, self.objectCounter)
            self.eventBus.publish(Event(EventType.ADD_GATE_INPUT_VIEW, payload))
            self.objectCounter += 1
        for idx in range(outputs):
            payload = (gateId, self.objectCounter)
            self.eventBus.publish(Event(EventType.ADD_GATE_OUTPUT_VIEW, payload))
            self.objectCounter += 1
        self.objectCounter += 1

    def addGateNodes(self, gate, lenGateInputs, lenGateOutputs):
        for idx in range(lenGateInputs):
            self.addInput(InputType.GATE_INPUT) 
        for idx in range(lenGateOutputs):
            self.addOutput(OutputType.GATE_OUTPUT)

    def linkNodes(self, payload):
        node1Id, node2Id = payload
        node1 = self.findById(node1Id)
        node2 = self.findById(node2Id)
        
        node2.input = node1
        node1.output = node2
        self.eventBus.publish(Event(EventType.LINK_NODES_VIEW, (node1.id, node2.id)))




