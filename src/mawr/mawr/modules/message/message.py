
class Message:
    def __init__(self):
        self.audio: list[list[int]] = []

    def add_part(self, part: list[int]):
        self.audio.extend(part)