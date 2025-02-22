from Port import Port, PortType
from Gate import Gate, GateType
from Event import EventType, Event, EventBus
from typing import Tuple

class Model:
    def __init__(self, eventBus: EventBus):
        self.eventBus = eventBus

        self.objects = {}
        self.objectCounter = 0

        self.portMap = {}
        self.gates = {}

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

        self.gates[gateId] = newGate

        return (newGate.id, newGate.numInputs, newGate.numOutputs)

    def addGatePorts(self, gateId):
        gate = self.objects[gateId]
        inputIds = []
        outputIds = []
        for idx in range(gate.numInputs):
            inputIds.append(self.addPort(PortType.GATE_INPUT, gateId)[0])
        for idx in range(gate.numOutputs):
            outputIds.append(self.addPort(PortType.GATE_OUTPUT, gateId)[0])
        return (inputIds, outputIds)

    def linkPorts(self, portIds):
        assert isinstance(portIds, tuple) and len(portIds) == 2 and all(isinstance(item, int) for item in portIds)
        port1Id, port2Id = portIds
        port1 = self.objects[port1Id]
        port2 = self.objects[port2Id]
        port2.input = port1
        port2.state = port1.state
        port1.output = port2
        
        self.portMap[port1Id] = port2Id 

    def runGates(self):
        for idx in self.gates.keys():
            gate = self.gates[idx]
            gate.run()

    def stateChange(self, portId):
        p = self.objects[portId]
        assert isinstance(portId, int)
        assert portId in self.objects.keys()
        assert p.state is not None
        p.state = not p.state

    def stateVerify(self):
        stateMap = {}
        for idx in self.portMap.keys():
            obj = self.objects[idx]
            outputId = self.portMap[idx] 
            output = self.objects[outputId]
            output.input = obj
            obj.output = output
            output.state = obj.state

            stateMap[obj.id] = obj.state
            stateMap[output.id] = output.state

        return stateMap



        


