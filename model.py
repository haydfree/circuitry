from node import Node, NodeType
from typing import List
from events import Event, EventType
from event_bus import EventBus


class Model:
    def __init__(self, eventBus: EventBus):
        self.inputs: List[Node] = []
        self.outputs: List[Node] = [] 
        self.eventBus = eventBus

    def addNode(self, nodeType: NodeType):
        nodeState: int = 0
        newNode: Node = Node(nodeType, nodeState)
        
        if nodeType == NodeType.INPUT:
            self.inputs.append(newNode)
            self.eventBus.publish(Event(EventType.ADD_INPUT_COMPLETE, newNode))
        else:
            self.outputs.append(newNode)
            self.eventBus.publish(Event(EventType.ADD_OUTPUT_COMPLETE, newNode))


