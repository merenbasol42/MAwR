import time
import pyaudio
from queue import Queue

def def_logger(text: str):
    print(f"Player said: {text}")

class Player:
    def __init__(self):
        self.__play_flag: bool = False
        self.__queue_flag: bool = False
        self.__queue: Queue | None = None 
        self.logger = def_logger 

    def load(self, audio: list[list[int]]):
        """Audio listesini kuyruk içerisine ekler."""
        self.__queue = Queue()  # Eğer kuyruk None ise, yeni bir kuyruk oluştur.

        # Audio listesindeki tüm elemanları kuyruğa ekliyoruz.
        for item in audio:
            self.__queue.put(bytes(item))

    def stop(self):
        self.__play_flag = False

    def start(self):
        if self.__play_flag:
            self.logger("::ERR:: already loaded an audio")
            return

        # PyAudio başlatma ve ses çalmak için gerekli parametreler
        p = pyaudio.PyAudio()

        # Ses çıkışı için bir stream açıyoruz
        stream = p.open(
            format = pyaudio.paInt16,
            channels = 1,
            rate = 44100,
            output = True,
            frames_per_buffer = 1024
        )

        self.logger("playing has been started")

        self.__play_flag = True
        while self.__play_flag:
            if not self.__queue.empty():
                data = self.__make_safe(lambda: self.__queue.get())
                # Kuyruktan alınan veriyi ses olarak çalıyoruz
                stream.write(data)
                self.logger("playing ...")
            else:
                self.__play_flag = False
        
        self.logger("playing has been end")
        stream.stop_stream()  # Akışı durduruyoruz
        stream.close()  # Akışı kapatıyoruz

    def __make_safe(self, func):
        while self.__queue_flag:pass
        self.__queue_flag = True
        res = func()
        self.__queue_flag = False
        return res