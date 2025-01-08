import customtkinter as ctk

def def_logger(text: str):
    print(
        f"User GUI said: {text}"
    )

class GUI:
    def __init__(self):
        self.wn: ctk.CTk = ctk.CTk()
        self.wn.title = "User" 
        self.logger = def_logger

        self.record_button: ctk.CTkButton
        self.play_button: ctk.CTkButton

    def __init_components(self):
        self.logger("components initializing")
        self.record_button = ctk.CTkButton(self.wn)
        self.play_button = ctk.CTkButton(self.wn)
        self.record_button.grid(row=0, column=0)
        self.record_button.grid(row=0, column=1)
        self.wn.grid_rowconfigure(0, weight=1)
        self.wn.grid_columnconfigure(0, weight=1)
        self.wn.grid_columnconfigure(1, weight=1)

    def run(self):
        self.__init_components()
        self.logger("running ...")
        self.wn.mainloop()