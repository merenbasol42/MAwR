import customtkinter as ctk
from commpy.event_pkg import Event
from commpy.std_ifs.msg import Bool, Int

class Buttons(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.record_button: ctk.CTkButton
        self.play_button: ctk.CTkButton

        self.play_state: False
        self.record_state: False
        
        self.e_play: Event[Int] = Event("play", Int)
        self.e_record: Event[Bool] = Event("record", Bool)

    def __cb_play_button(self):
        print("Play button pressed")
        if self.play_state:
            self.play_button.configure(text="play")
            self.e_play.trigger(-1) 
        else:
            self.play_button.configure(text="pause")
            self.e_play.trigger(0) 
    
        self.play_state = not self.play_state

    def __cb_record_button_pressed(self):
        print("Record button pressed")
        if self.record_state:
            self.record_button.configure(text="record")
            self.e_record.trigger(False)
        else:
            self.record_button.configure(text="save")
            self.e_record.trigger(True)
        
        self.record_state = not self.record_state

    def create(self):
        self.record_button = ctk.CTkButton(self, text="record", command=self.__cb_record_button_pressed)
        self.play_button = ctk.CTkButton(self, text="play", command=self.__cb_play_button)

        # self.record_button.bind("<ButtonRelease-1>", lambda e: self.__cb_record_button_released())

    def insert(self):
        self.record_button.grid(row=0, column=0)
        self.play_button.grid(row=0, column=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
