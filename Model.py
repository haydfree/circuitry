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

    def addInput(self):
        state = 0
        newInput = Input(state)
        
        self.inputs.append(newInput)
        self.eventBus.publish(Event(EventType.ADD_INPUT_VIEW, newInput))

    def addOutput(self):
        state = 0
        newOutput = Output(state)

        self.outputs.append(newOutput)
        self.eventBus.publish(Event(EventType.ADD_OUTPUT_VIEW, newOutput))

    def addGate(self, gateType: GateType):
        if gateType == GateType.NOT_GATE:
            text = "NOT GATE"
            inputs = 1
            outputs = 1
            newGate = Gate(gateType, text)
            self.eventBus.publish(Event(EventType.ADD_NOT_GATE_VIEW, (text, inputs, outputs)))
        if gateType == GateType.AND_GATE:
            text = "AND GATE"
            inputs = 2
            outputs = 1
            newGate = Gate(gateType, text)
            self.eventBus.publish(Event(EventType.ADD_AND_GATE_VIEW, (text, inputs, outputs)))




