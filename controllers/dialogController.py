from models.message import Message


class DialogController:
    def __init__(self):
        self.messages = []

    def hasMessages(self):
        return len(self.messages) > 0

    def pop(self):
        response = self.first().callback()
        self.messages.pop(0)

        print(response)
        if response:
            for message in response:
                self.messages.insert(0, Message(message))

    def first(self):
        return self.messages[0]

    def addMessage(self, message):
        self.messages.append(message)
