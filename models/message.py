class Message:
    def __init__(self, text, callback = lambda: None):
        self.text = text
        self.callback = callback