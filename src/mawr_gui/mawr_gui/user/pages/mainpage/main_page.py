import customtkinter as ctk
from commpy.event_pkg import Event
from commpy.std_ifs.msg import Bool, Int

from .buttons import Buttons
from ..ipage import IPage

class MainPage(IPage):
    def __init__(self, master):
        super().__init__(master)
        self.buttons: Buttons = Buttons(self)

        self.e_play: Event[Int] = self.buttons.e_play
        self.e_record: Event[Bool] = self.buttons.e_record

    def create(self):
        self.buttons.create()

    def insert(self):
        self.buttons.insert()
        self.buttons.grid(row=0, column=0)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        