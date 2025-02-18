class DialogController:
    def __init__(self):
        self.messages = []

    def hasMessages(self):
        return len(self.messages) > 0

    def pop(self):
        self.messages.pop(0)

    def first(self):
        return self.messages[0]

    def addMessage(self, message):
        self.messages.append(message)