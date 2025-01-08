import customtkinter as ctk
from commpy.event_pkg import Event

class MainPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.record_button: ctk.CTkButton
        self.play_button: ctk.CTkButton
        self.e_play: Event = Event("play")
        self.e_record: Event = Event("record")

    def create(self):
        self.record_button = ctk.CTkButton(self, text="record")
        self.play_button = ctk.CTkButton(self, text="play")

    def insert(self):
        self.record_button.grid(row=0, column=0)
        self.play_button.grid(row=0, column=1)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)