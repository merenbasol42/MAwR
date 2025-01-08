import pyaudio
from queue import Queue
from threading import Thread

class Recorder:
    def __init__(self):
        self.__record_flag: bool = False
        self.__queue_flag: bool = False
        self.__queue: Queue = Queue()

    def get_audio(self) -> list[int]:
        return list(self.__queue.queue)

    def stop(self):
        self.__record_flag = False

    def start(self, thread: bool = True):
        if thread: Thread(
            target = self.__start,
            daemon = True
            ).start()
        else: self.__start()

    def __start(self):
        # Ses kaydı parametreleri
        FORMAT = pyaudio.paInt16  # Ses formatı
        CHANNELS = 1  # Mono ses
        RATE = 44100  # Sampling rate
        CHUNK = 1024  # Ses verisi boyutu

        p = pyaudio.PyAudio()

        # Ses akışını başlatıyoruz
        stream = p.open(
            rate = RATE,
            input = True,
            format = FORMAT,
            channels = CHANNELS,
            frames_per_buffer = CHUNK
        )

        self.__record_flag = True
        while self.__record_flag:
            data = stream.read(CHUNK, exception_on_overflow=False)
            # Veriyi kuyruğa ekliyoruz
            self.__make_safe(lambda: self.__queue.put(data[:]))
        
        stream.stop_stream()  # Akışı durduruyoruz
        stream.close()  # Akışı kapatıyoruz

    def __make_safe(self, func) -> ...:
        while self.__queue_flag: pass
        self.__queue_flag = True
        res = func()
        self.__queue_flag = False
        return res