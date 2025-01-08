import customtkinter as ctk
from commpy.event_pkg import Event
from commpy.std_ifs.msg import String

class RegistirationPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.text_box: ctk.CTkEntry
        self.submit_button: ctk.CTkButton

        self.e_name: Event[String] = Event("name", String)

    def __cb_submit_button(self):
        self.e_name.trigger(self.text_box.get())

    def create(self):
        self.text_box = ctk.CTkEntry(self)
        self.submit_button = ctk.CTkButton(
            self,
            text = "submit",
            command = self.__cb_submit_button
        )
        
    def insert(self):        
        self.text_box.grid(row=0, column=0)
        self.submit_button.grid(row=1, column=0)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

