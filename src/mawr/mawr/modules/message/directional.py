from .message import Message

class DirectionalMessage(Message):
    def __init__(self, from_: str = None, to_: str = None):
        super().__init__()
        self.from_: str = None
        self.to_: str = None
    