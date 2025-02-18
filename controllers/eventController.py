from pygame import event, QUIT
from utils.constants import EVENTS, KEYDOWN


class EventController:

    def __init__(self):
        self.observers = []

    def subscribe(self, observer):
        self.observers.append(observer)

    def unsubscribe(self, observer):
        self.observers.remove(observer)

    def unsubscribeAll(self):
        self.observers = []

    def validateInputs(self):
        pass

    def close(self):
        self.emitEvent(EVENTS.QUIT)

    def emitEvent(self, event, payload = None):
        for ob in self.observers:
            if (ob[0] == event):
                if (payload == None):
                    ob[1]()
                else:
                    ob[1](payload)

    def checkEvents(self):
        for _event in event.get():
            if _event.type == QUIT:
                self.emitEvent(EVENTS.QUIT)
            if _event.type == EVENTS.KEYDOWN:
                self.emitEvent(EVENTS.MENU_CONTROLLER, _event)