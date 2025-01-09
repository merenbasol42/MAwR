
class Message:
    def __init__(self):
        self.audio: list[list[int]] = []

    def add_part(self, part: list[list[int]]):
        self.audio.extend(part)

    def add_frame(self, frame: list[int]):
        self.audio.append(frame)