import customtkinter as ctk
from commpy.event_pkg import Event
from commpy.std_ifs.msg import Bool, Int

class MainPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.record_button: ctk.CTkButton
        self.play_button: ctk.CTkButton
        self.togg = True
        self.e_play: Event[Int] = Event("play", Int)
        self.e_record: Event[Bool] = Event("record", Bool)

    def __cb_play_button(self):
        print("Play button pressed")
        self.e_play.trigger(0) 
    
    def __cb_record_button_pressed(self):
        print("Record button pressed")
        self.e_record.trigger(self.togg)
        self.togg = not self.togg 

    def __cb_record_button_released(self):
        print("Record button released")
        self.e_record.trigger(False)

    def create(self):
        self.record_button = ctk.CTkButton(self, text="Record", command=self.__cb_record_button_pressed)
        self.play_button = ctk.CTkButton(self, text="Play", command=self.__cb_play_button)

        # self.record_button.bind("<ButtonRelease-1>", lambda e: self.__cb_record_button_released())

    def insert(self):
        self.record_button.grid(row=0, column=0)
        self.play_button.grid(row=0, column=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
