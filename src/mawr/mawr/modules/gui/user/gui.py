import customtkinter as ctk

def def_logger(text: str):
    print(
        f"User GUI said: {text}"
    )

class GUI:
    def __init__(self):
        self.wn: ctk.CTk
        self.logger = def_logger

        self.record_button: ctk.CTkButton
        self.play_button: ctk.CTkButton
    
    def __init_wn(self):
        self.wn: ctk.CTk = ctk.CTk()
        self.wn.title = "User" 
        self.wn.geometry("400x400")

    def __init_components(self):
        self.logger("components initializing")
        self.record_button = ctk.CTkButton(self.wn, text="record")
        self.play_button = ctk.CTkButton(self.wn, text="play")
        self.record_button.grid(row=0, column=0)
        self.play_button.grid(row=0, column=1)
        self.wn.grid_rowconfigure(0, weight=1)
        self.wn.grid_columnconfigure(0, weight=1)
        self.wn.grid_columnconfigure(1, weight=1)

    def init(self):
        self.__init_wn()
        self.__init_components()

    def run(self):
        self.logger("running ...")
        self.wn.mainloop()