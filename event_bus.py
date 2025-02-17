from events import Event, EventType


class EventBus:
    def __init__(self):
        self.subscribers = [] 

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    def publish(self, event: Event):
        for subscriber in self.subscribers:
            subscriber.handleEvent(event)


