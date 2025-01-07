
class Message:
    def __init__(self):
        self.audio: list[int]

    def add_part(self, voice: list[int]):
        self.audio.extend(voice)

    def diss_assemble(self, piece_len: int) -> list:        
        result = []
        counter = 0

        while counter < len(self.audio):
            result.append(
                [
                    self.audio[
                        counter
                        : 
                        counter + piece_len
                    ].copy()
                ]
            )
            counter += piece_len

        return result