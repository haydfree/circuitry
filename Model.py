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
        port1Id, port2Id = portIds
        port1 = self.objects[port1Id]
        port2 = self.objects[port2Id]
        port2.input = port1
        port2.state = port1.state
        port1.output = port2

    def stateChange(self, portId):
        p = self.objects[portId]
        p.state = not p.state

    def stateVerify(self):
        stateMap = {}
        for idx in self.objects.keys():
            obj = self.objects[idx]
            if type(obj) is Port:
                if obj.type == PortType.CIRCUIT_INPUT:
                    if obj.output is not None:
                        obj.output.state = obj.state
                elif obj.type == PortType.CIRCUIT_OUTPUT:
                    if obj.input is not None:
                        obj.state = obj.input.state
                elif obj.type == PortType.GATE_INPUT:
                    if obj.input is not None:
                        obj.state = obj.input.state
                     
            elif type(obj) is GateType:
                if obj.inputIds and obj.outputIds:
                    obj.run()

                stateMap[obj.id] = obj.state
        return stateMap
        


