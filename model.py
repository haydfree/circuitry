from node import Node
from typing import List
from events import Event, EventType
from event_bus import EventBus


class Model:
    def __init__(self, eventBus: EventBus):
        self.inputs: List[Node] = []
        self.outputs: List[Node] = [] 
        self.eventBus = eventBus

    def addInput(self):
        nodeType: int = 0
        nodeState: int = 0
        newNode: Node = Node(nodeType, nodeState)
        self.inputs.append(newNode)
        self.eventBus.publish(Event(EventType.ADD_INPUT_COMPLETE, newNode))


