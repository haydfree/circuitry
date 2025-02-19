from Input import Input
from Output import Output
from Gate import Gate
from Event import EventType, Event, EventBus
from GateType import GateType
from NodeType import NodeType

class Model:
    def __init__(self, eventBus: EventBus):
        self.eventBus = eventBus

        self.inputs = []
        self.outputs = [] 
        self.gates = []

    def addInput(self, inputId):
        state = 0
        newInput = Input(inputId, state, None, None)
        
        self.inputs.append(newInput)
        self.eventBus.publish(Event(EventType.ADD_INPUT_VIEW, newInput))

    def addOutput(self, outputId):
        state = 0
        newOutput = Output(outputId, state, None, None)

        self.outputs.append(newOutput)
        self.eventBus.publish(Event(EventType.ADD_OUTPUT_VIEW, newOutput))

    def addGate(self, gateType: GateType):
        if gateType == GateType.NOT_GATE:
            text = "NOT GATE"
            inputs = 1
            outputs = 1
            newGate = Gate(gateType, text)
            self.gates.append(newGate)
            self.eventBus.publish(Event(EventType.ADD_NOT_GATE_VIEW, (text, inputs, outputs)))
        if gateType == GateType.AND_GATE:
            text = "AND GATE"
            inputs = 2
            outputs = 1
            newGate = Gate(gateType, text)
                for idx in range(0, inputs):
                    newGate.inputs.append(Input())
            self.gates.append(newGate)
            self.eventBus.publish(Event(EventType.ADD_AND_GATE_VIEW, (text, inputs, outputs)))

    def linkNodes(self, node1Id, node2Id):
        print(node1Id, node2Id)
        node1 = None
        node2 = None
        for inp in self.inputs:
            if inp.id == node1Id:
                node1 = inp
            if inp.id == node2Id:
                node2 = inp
        for out in self.outputs:
            if out.id == node1Id:
                node1 = out
            if out.id == node2Id:
                node2 = out
        for gate in self.gates:
            for inp in gate.inputs:
                if inp.id == node1Id:
                    node1 = inp
                if inp.id == node2Id:
                    node2 = inp
            for out in gate.outputs:
                if out.id == node1Id:
                    node1 = out
                if out.id == node2Id:
                    node2 = out
        print(node1, node2)
        
        node2.input = node1
        node1.output = node2
        self.eventBus.publish(Event(EventType.LINK_NODES_VIEW, (node1.id, node2.id)))




