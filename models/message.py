class Message:
    def __init__(self, text, callback = lambda: None, payload = None):
        self.text = text
        self.callback = callback